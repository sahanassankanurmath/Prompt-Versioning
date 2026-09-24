import uuid
import pandas as pd
import streamlit as st

from versioning import create_prompt, create_new_version, list_prompts, list_versions
from routing import assign_version
from llm_client import run_prompt_version
from evaluation import score_basic
from experiments import create_experiment, list_experiments, log_result, get_results
from stats_utils import check_significance

st.set_page_config(page_title="Prompt A/B Platform", layout="wide")

# One fake "session_id" per browser tab, so the router has something to hash on
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

page = st.sidebar.radio("Navigate", ["1. Prompts", "2. Experiments", "3. Run & Test", "4. Dashboard"])

# ---------------- Page 1: Prompts ----------------
if page == "1. Prompts":
    st.header("Prompts & versions")

    with st.form("new_prompt"):
        name = st.text_input("New prompt name (e.g. 'Support greeting')")
        if st.form_submit_button("Create prompt") and name:
            create_prompt(name)
            st.success(f"Created prompt '{name}'")
            st.rerun()

    prompts = list_prompts()
    if not prompts:
        st.info("No prompts yet - create one above.")
    for p in prompts:
        with st.expander(f"{p['name']} (id {p['id']})"):
            with st.form(f"version_form_{p['id']}"):
                content = st.text_area(
                    "Prompt content (use {input} as the placeholder for user input)",
                    key=f"content_{p['id']}",
                )
                note = st.text_input("Change note", key=f"note_{p['id']}")
                if st.form_submit_button("Save new version") and content:
                    create_new_version(p["id"], content, note)
                    st.success("Version saved")
                    st.rerun()

            versions = list_versions(p["id"])
            if versions:
                st.dataframe(pd.DataFrame(versions)[["version_number", "content", "change_note", "created_at"]])

# ---------------- Page 2: Experiments ----------------
elif page == "2. Experiments":
    st.header("Create an experiment")
    prompts = list_prompts()
    if not prompts:
        st.warning("Create a prompt with at least 2 versions first.")
    else:
        prompt_names = {p["id"]: p["name"] for p in prompts}
        selected_id = st.selectbox("Prompt", options=list(prompt_names), format_func=lambda x: prompt_names[x])
        versions = list_versions(selected_id)
        if len(versions) < 2:
            st.warning("This prompt needs at least 2 versions before you can A/B test it.")
        else:
            version_labels = {v["id"]: f"v{v['version_number']} - {v['content'][:40]}..." for v in versions}
            col1, col2 = st.columns(2)
            with col1:
                version_a = st.selectbox("Version A", options=list(version_labels), format_func=lambda x: version_labels[x])
            with col2:
                version_b = st.selectbox("Version B", options=list(version_labels), format_func=lambda x: version_labels[x])
            if st.button("Start experiment") and version_a != version_b:
                exp_id = create_experiment(selected_id, version_a, version_b)
                st.success(f"Experiment #{exp_id} created")

    st.divider()
    st.subheader("Existing experiments")
    st.dataframe(pd.DataFrame(list_experiments()))

# ---------------- Page 3: Run & Test ----------------
elif page == "3. Run & Test":
    st.header("Send a test request through the router")
    experiments = list_experiments()
    if not experiments:
        st.warning("Create an experiment first.")
    else:
        exp_map = {e["id"]: e for e in experiments}
        exp_id = st.selectbox("Experiment", options=list(exp_map))
        user_input = st.text_input("Test input")

        if st.button("Run") and user_input:
            exp = exp_map[exp_id]
            assigned = assign_version(st.session_state.session_id, exp_id)
            version_id = exp["version_a_id"] if assigned == "A" else exp["version_b_id"]

            versions = list_versions(exp["prompt_id"])
            version_content = next(v["content"] for v in versions if v["id"] == version_id)

            result = run_prompt_version(version_content, user_input)
            if result["error"]:
                st.error(f"LLM call failed: {result['error']}")
            else:
                score = score_basic(result["output"])
                log_result(
                    exp_id, version_id, st.session_state.session_id,
                    user_input, result["output"], result["latency_ms"],
                    result["token_count"], score,
                )
                st.write(f"Routed to version **{assigned}**")
                st.write(result["output"])
                st.caption(f"Latency: {result['latency_ms']}ms | Tokens: {result['token_count']} | Score: {score}")

# ---------------- Page 4: Dashboard ----------------
elif page == "4. Dashboard":
    st.header("Experiment results")
    experiments = list_experiments()
    if not experiments:
        st.warning("No experiments yet.")
    else:
        exp_map = {e["id"]: e for e in experiments}
        exp_id = st.selectbox("Experiment", options=list(exp_map))
        exp = exp_map[exp_id]
        results = get_results(exp_id)

        if not results:
            st.info("No results logged yet - go to 'Run & Test' and send some requests.")
        else:
            df = pd.DataFrame(results)
            scores_a = df[df.version_id == exp["version_a_id"]]["score"].tolist()
            scores_b = df[df.version_id == exp["version_b_id"]]["score"].tolist()

            col1, col2 = st.columns(2)
            col1.metric("Version A mean score", f"{sum(scores_a)/len(scores_a):.2f}" if scores_a else "n/a")
            col2.metric("Version B mean score", f"{sum(scores_b)/len(scores_b):.2f}" if scores_b else "n/a")

            sig = check_significance(scores_a, scores_b)
            if sig.get("p_value") is not None:
                st.metric("p-value", f"{sig['p_value']:.4f}")
                st.write("✅ Statistically significant difference" if sig["significant"] else "⏳ Not yet significant - keep collecting data")
            else:
                st.info(sig.get("note", "Not enough data yet"))

            st.subheader("Raw results")
            st.dataframe(df)