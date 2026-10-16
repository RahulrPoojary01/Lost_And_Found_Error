CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(150) NOT NULL,
    date VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE claims (
    id SERIAL PRIMARY KEY,
    item_id INT REFERENCES items(id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    year VARCHAR(20) NOT NULL,
    usn VARCHAR(50) NOT NULL,
    claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO items (title, category, location, date, description, image_url, status) VALUES 
('MacBook Pro M1 (Space Gray)', 'Electronics', 'Central Library 2nd Floor', 'Oct 14, 2026', 'Left on desk near window. Has a sticker on top lid.', 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80', 'Available'),
('Leather Wallet with Student ID', 'Valuables', 'Main Cafeteria Table 12', 'Oct 15, 2026', 'Brown leather wallet containing cash and ID card.', 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=600&auto=format&fit=crop&q=80', 'Available'),
('Hydro Flask Water Bottle (Sage Green)', 'Miscellaneous', 'Sports Complex Turf', 'Oct 13, 2026', 'Matte green 32oz bottle with stickers near the bench.', 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80', 'Available');