CREATE DATABASE IF NOT EXISTS prompt_project_db;
USE prompt_project_db;

CREATE TABLE IF NOT EXISTS prompts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prompt_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prompt_id INT NOT NULL,
    version_number INT NOT NULL,
    content TEXT NOT NULL,
    change_note VARCHAR(500) NOT NULL DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_prompt_versions_prompt
        FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
    CONSTRAINT uq_prompt_version UNIQUE (prompt_id, version_number)
);

CREATE TABLE IF NOT EXISTS experiments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prompt_id INT NOT NULL,
    version_a_id INT NOT NULL,
    version_b_id INT NOT NULL,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_experiments_prompt
        FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
    CONSTRAINT fk_experiments_version_a
        FOREIGN KEY (version_a_id) REFERENCES prompt_versions(id),
    CONSTRAINT fk_experiments_version_b
        FOREIGN KEY (version_b_id) REFERENCES prompt_versions(id)
);

CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_id INT NOT NULL,
    version_id INT NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    input_text TEXT NOT NULL,
    output_text TEXT NOT NULL,
    latency_ms INT NOT NULL,
    token_count INT NOT NULL,
    score DECIMAL(10, 4) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_results_experiment
        FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE,
    CONSTRAINT fk_results_version
        FOREIGN KEY (version_id) REFERENCES prompt_versions(id)
);