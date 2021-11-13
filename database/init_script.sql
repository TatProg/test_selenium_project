CREATE TABLE IF NOT EXISTS addresses
(
    address_id        INT PRIMARY KEY,
    KindPremises      VARCHAR(64),
    Adress_PostCode   VARCHAR(64),
    Adress_Region     VARCHAR(64),
    Adress_TypeCity   VARCHAR(64),
    Adress_City       VARCHAR(64),
    Adress_TypeStreet VARCHAR(64),
    Adress_Street     VARCHAR(64),
    Adress_House      VARCHAR(64),
    Adress_Block      VARCHAR(64),
    Adress_Flat       VARCHAR(64),
    Adress            TEXT
);

CREATE TABLE IF NOT EXISTS house_information
(
    house_id             INT PRIMARY KEY,
    status               BOOLEAN, --todo решить, убрать или оставить
    year_of_occupancy    INT,
    number_of_floors     INT,
    last_update          VARCHAR(64),
    type_of_construction VARCHAR(64),
    house_type           VARCHAR(64),
    wreck_status         BOOLEAN,
    cadastral_number     VARCHAR(64),
    type_of_ceilings     VARCHAR(64),
    walls_material       VARCHAR(64),
    FOREIGN KEY (house_id) REFERENCES addresses (address_id)
);

-- DROP TABLE addresses;
-- DROP TABLE house_information;