CREATE TABLE "favors" (
  "id" serial PRIMARY KEY,
  "name" text,
  "description" text,
  "jollies" int,
  "cost" int,
  "type" text
);

CREATE TABLE "games" (
  "id" serial PRIMARY KEY,
  "name" text,
  "created" timestamp
);

CREATE TABLE "exchanges" (
  "id" serial PRIMARY KEY,
  "game_id" int,
  "favor_id" int,
  "giving_player" int,
  "receiving_player" int,
  "verified" bool,
  "created" timestamp
);

CREATE TABLE "players" (
  "id" serial PRIMARY KEY,
  "name" text,
  "game_id" int,
  "money" int
);

CREATE TABLE "posts" (
  "id" serial PRIMARY KEY,
  "name" text,
  "type" text,
  "favor_id" int,
  "game_id" int,
  "poster" int,
  "created" timestamp
);

COMMENT ON COLUMN "posts"."type" IS 'Want to give or want to get?';

ALTER TABLE "exchanges" ADD FOREIGN KEY ("game_id") REFERENCES "games" ("id");

ALTER TABLE "exchanges" ADD FOREIGN KEY ("favor_id") REFERENCES "favors" ("id");

ALTER TABLE "exchanges" ADD FOREIGN KEY ("giving_player") REFERENCES "players" ("id");

ALTER TABLE "exchanges" ADD FOREIGN KEY ("receiving_player") REFERENCES "players" ("id");

ALTER TABLE "players" ADD FOREIGN KEY ("game_id") REFERENCES "games" ("id");

ALTER TABLE "posts" ADD FOREIGN KEY ("favor_id") REFERENCES "favors" ("id");

ALTER TABLE "posts" ADD FOREIGN KEY ("game_id") REFERENCES "games" ("id");

ALTER TABLE "posts" ADD FOREIGN KEY ("poster") REFERENCES "players" ("id");