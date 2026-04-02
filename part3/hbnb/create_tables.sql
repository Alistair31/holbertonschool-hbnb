-- =============================================================
-- HBnB - SQL Script: Table Creation and Initial Data
-- =============================================================

-- launch the script with:
-- sqlite3 instance/development.db < create_tables.sql

-- -------------------------------------------------------------
-- Table: users
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id          CHAR(36)     PRIMARY KEY,
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50)  NOT NULL,
    email       VARCHAR(120) NOT NULL UNIQUE,
    password    VARCHAR(128) NOT NULL,
    is_admin    BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------------
-- Table: places
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS places (
    id          CHAR(36)     PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    description TEXT         NOT NULL,
    price       DECIMAL(10,2) NOT NULL,
    latitude    FLOAT        NOT NULL,
    longitude   FLOAT        NOT NULL,
    owner_id    CHAR(36)     NOT NULL,
    image_url   VARCHAR(255),
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- -------------------------------------------------------------
-- Table: amenities
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS amenities (
    id         CHAR(36)     PRIMARY KEY,
    name       VARCHAR(100) NOT NULL UNIQUE,
    icon       VARCHAR(10)  DEFAULT '🏠',
    icon_url   VARCHAR(255),
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------------
-- Table: reviews
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
    id         CHAR(36)  PRIMARY KEY,
    text       TEXT      NOT NULL,
    rating     INTEGER   NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id    CHAR(36)  NOT NULL,
    place_id   CHAR(36)  NOT NULL,
    created_at DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

-- -------------------------------------------------------------
-- Table: place_images
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS place_images (
    id         CHAR(36)     PRIMARY KEY,
    place_id   CHAR(36)     NOT NULL,
    image_url  VARCHAR(255) NOT NULL,
    is_primary BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
);

-- -------------------------------------------------------------
-- Table: place_amenity (junction many-to-many)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id   CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id)   REFERENCES places(id)    ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- =============================================================
-- Initial Data
-- =============================================================

-- Admin user (password: admin1234 — bcrypt hashed)
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$R3I/C.C8rpkdKSq7sswzI.KsD3/GCZiXJkRWu1LZaCHXUaeiCX.e2',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Initial amenities
INSERT OR IGNORE INTO amenities (id, name, icon, created_at, updated_at)
VALUES
    ('eb40c852-327d-4f05-b695-ce57c9ad9940', 'WiFi',            '📶', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('16b54b85-efc9-4932-93b0-87ed5d5fb812', 'Swimming Pool',   '🏊', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('9841a170-da50-4e72-8741-175ae737441f', 'Air Conditioning', '❄️', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
