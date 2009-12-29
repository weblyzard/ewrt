-- creates the countryinfo table

CREATE TABLE countryinfo (
  id           bigint PRIMARY KEY REFERENCES gazetteerentity,
  areaInSqKm   float,
  population   integer
);
