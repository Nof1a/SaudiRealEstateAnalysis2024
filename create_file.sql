use databaserealstate;

-- Create Locations Table
CREATE TABLE Locations (
    id INT PRIMARY KEY,
    region_id INT NOT NULL,
    region_name VARCHAR(255) NOT NULL,
    longitude DECIMAL(10, 5) NOT NULL,
    latitude DECIMAL(10, 5) NOT NULL,
    INDEX (region_id)  -- Add an index to the region_id column
);

-- Create RealEstate Table
CREATE TABLE RealEstate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region_id INT NOT NULL,
    region_name VARCHAR(255),
    month VARCHAR(255),
    property_type VARCHAR(255),
    price_sar DECIMAL(20, 2) NOT NULL,
    area_sqm DECIMAL(20, 2) NOT NULL,
    transaction_count INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Locations(region_id)
);

 

 

select * from locations;

