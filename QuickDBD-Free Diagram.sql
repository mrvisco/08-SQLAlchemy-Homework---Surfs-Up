-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/sKlOlU
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

CREATE TABLE "station" (
    "station" varchar(15)   NOT NULL,
    "name" varchar(50)   NOT NULL,
    "latitude" float,
    "longitude" float,
    "elevarion" float,
    CONSTRAINT "pk_station" PRIMARY KEY (
        "station"
     )
);

CREATE TABLE "measurement" (
    "station" varchar(15)   NOT NULL,
    "date" varchar(15)   NOT NULL,
    "pecp" float,
    "tobs" float
);

ALTER TABLE "measurement" ADD CONSTRAINT "fk_measurement_station" FOREIGN KEY("station")
REFERENCES "station" ("station");

