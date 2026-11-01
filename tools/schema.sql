-- Aplus worksheets: tables (run once in phpMyAdmin)
-- All rows are keyed by natural keys (country / subject / grade / slug),
-- so content can be re-imported any number of times with REPLACE INTO.

CREATE TABLE IF NOT EXISTS ws_country (
  code      VARCHAR(8)   NOT NULL PRIMARY KEY,   -- us, uk, au ...
  name      VARCHAR(80)  NOT NULL,               -- United States
  lang      VARCHAR(8)   NOT NULL DEFAULT 'en',  -- page language
  hreflang  VARCHAR(12)  NOT NULL DEFAULT 'en',  -- en-us
  paper     VARCHAR(8)   NOT NULL DEFAULT 'a4',  -- letter | a4
  standard  VARCHAR(120) NOT NULL DEFAULT '',    -- Common Core State Standards
  intro     TEXT,
  sort      INT          NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ws_subject (
  country   VARCHAR(8)   NOT NULL,
  slug      VARCHAR(40)  NOT NULL,               -- math
  name      VARCHAR(80)  NOT NULL,               -- Math
  intro     TEXT,
  sort      INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (country, slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ws_grade (
  country   VARCHAR(8)   NOT NULL,
  subject   VARCHAR(40)  NOT NULL,
  slug      VARCHAR(40)  NOT NULL,               -- grade-3
  name      VARCHAR(80)  NOT NULL,               -- Grade 3
  intro     TEXT,
  sort      INT          NOT NULL DEFAULT 0,
  PRIMARY KEY (country, subject, slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ws_unit (
  country       VARCHAR(8)   NOT NULL,
  subject       VARCHAR(40)  NOT NULL,
  grade         VARCHAR(40)  NOT NULL,
  slug          VARCHAR(80)  NOT NULL,           -- multiplication-facts
  title         VARCHAR(200) NOT NULL,           -- H1
  seo_title     VARCHAR(200) NOT NULL DEFAULT '',-- <title>
  short_title   VARCHAR(120) NOT NULL DEFAULT '',
  domain        VARCHAR(120) NOT NULL DEFAULT '',-- group heading on the grade page
  standard_code VARCHAR(40)  NOT NULL DEFAULT '',-- 3.OA.C.7
  standard_url  VARCHAR(255) NOT NULL DEFAULT '',
  standard_text TEXT,
  meta_desc     TEXT,
  key_big       TEXT,
  key_sub       TEXT,
  body_html     MEDIUMTEXT,
  faq_json      MEDIUMTEXT,
  sets_json     MEDIUMTEXT,                      -- 5 sets x 20 questions
  pdf_url       VARCHAR(255) NOT NULL DEFAULT '',-- optional (R2 etc.)
  sort          INT          NOT NULL DEFAULT 0,
  updated       DATE,
  PRIMARY KEY (country, subject, grade, slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
