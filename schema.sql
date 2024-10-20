-- Create the Part table in the plm schema
CREATE TABLE plm.Part (
    part_id SERIAL PRIMARY KEY,
    part_name VARCHAR(255) NOT NULL,
    part_number VARCHAR(50) NOT NULL UNIQUE,
    quantity INTEGER NOT NULL,
    lifecycle_state VARCHAR(50) NOT NULL
);

-- Create the Drawing table in the plm schema
CREATE TABLE plm.Drawing (
    drawing_id SERIAL PRIMARY KEY,
    approved_by VARCHAR(255),
    drawing_title VARCHAR(255) NOT NULL,
    part_id INTEGER NOT NULL,
    state VARCHAR(50) NOT NULL,
    FOREIGN KEY (part_id) REFERENCES plm.Part(part_id) ON DELETE CASCADE
);

-- Optional: Add indexes for better performance
CREATE INDEX idx_part_number ON plm.Part(part_number);
CREATE INDEX idx_drawing_part_id ON plm.Drawing(part_id);