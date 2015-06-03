--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.0
-- Dumped by pg_dump version 9.4.1
-- Started on 2015-04-10 22:56:20 NOVT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE yandexdirect;
--
-- TOC entry 2068 (class 1262 OID 70724)
-- Name: yandexdirect; Type: DATABASE; Schema: -; Owner: yadirect
--

CREATE DATABASE yandexdirect WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ru_RU.utf8' LC_CTYPE = 'ru_RU.utf8';


ALTER DATABASE yandexdirect OWNER TO yadirect;

\connect yandexdirect

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 6 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 2069 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 177 (class 3079 OID 11897)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2071 (class 0 OID 0)
-- Dependencies: 177
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 174 (class 1259 OID 70797)
-- Name: banners; Type: TABLE; Schema: public; Owner: yadirect; Tablespace: 
--

CREATE TABLE banners (
    adgroupid integer,
    bannerid integer NOT NULL,
    statusarchive boolean,
    statusactivating character varying(40),
    title character varying(255),
    text character varying(1024),
    campaignid integer NOT NULL,
    isactive boolean,
    startdate date DEFAULT now()
);


ALTER TABLE banners OWNER TO yadirect;

--
-- TOC entry 173 (class 1259 OID 70769)
-- Name: campaigns; Type: TABLE; Schema: public; Owner: yadirect; Tablespace: 
--

CREATE TABLE campaigns (
    login character varying(120) NOT NULL,
    managername character varying(120),
    strategyname character varying(60),
    startdate date,
    daybudgetenabled boolean,
    contextstrategyname character varying(60),
    sum money,
    agencyname character varying(120),
    sumavailablefortransfer money,
    name character varying(255),
    clicks integer,
    statusshow boolean,
    campaigncurrency character varying(120),
    statusmoderate character varying(40),
    statusactivating character varying(40),
    shows integer,
    rest integer,
    campaignid integer NOT NULL,
    isactive boolean,
    statusarchive boolean,
    status character varying(250)
);


ALTER TABLE campaigns OWNER TO yadirect;

--
-- TOC entry 172 (class 1259 OID 70743)
-- Name: clients; Type: TABLE; Schema: public; Owner: yadirect; Tablespace: 
--

CREATE TABLE clients (
    sendaccnews boolean DEFAULT false,
    login character varying(120) DEFAULT ''::character varying NOT NULL,
    sharedaccountenabled boolean DEFAULT false,
    fio character varying(250) DEFAULT ''::character varying,
    datecreate date,
    displaystorerating boolean,
    sendwarn boolean DEFAULT false,
    email character varying(120),
    vatrate integer,
    phone character varying(60),
    role character(60),
    overdraftsumavailable integer,
    statusarch boolean,
    clientcurrencies character varying(60),
    sendnews boolean,
    nonresident boolean,
    discount integer
);


ALTER TABLE clients OWNER TO yadirect;

--
-- TOC entry 175 (class 1259 OID 70826)
-- Name: phrases; Type: TABLE; Schema: public; Owner: yadirect; Tablespace: 
--

CREATE TABLE phrases (
    statusphrasemoderate character varying(40),
    autobroker boolean,
    isrubric boolean,
    contextprice character varying(40),
    phraseid integer NOT NULL,
    adgroupid integer,
    campaignid integer,
    price money,
    bannerid integer NOT NULL,
    phrase character varying(250),
    autobudgetpriority character varying(40),
    statuspaused boolean
);


ALTER TABLE phrases OWNER TO yadirect;

--
-- TOC entry 176 (class 1259 OID 70872)
-- Name: statistic; Type: TABLE; Schema: public; Owner: yadirect; Tablespace: 
--

CREATE TABLE statistic (
    campaignid integer NOT NULL,
    bannerid integer NOT NULL,
    clicks integer,
    showscontext integer,
    sumcontext real,
    sumsearch real,
    clickscontext integer,
    shows integer,
    clickssearch integer,
    sum real,
    showssearch integer,
    statdate date NOT NULL
);


ALTER TABLE statistic OWNER TO yadirect;

--
-- TOC entry 1950 (class 2606 OID 70804)
-- Name: Banners_pkey; Type: CONSTRAINT; Schema: public; Owner: yadirect; Tablespace: 
--

ALTER TABLE ONLY banners
    ADD CONSTRAINT "Banners_pkey" PRIMARY KEY (campaignid, bannerid);


--
-- TOC entry 1948 (class 2606 OID 70777)
-- Name: Campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: yadirect; Tablespace: 
--

ALTER TABLE ONLY campaigns
    ADD CONSTRAINT "Campaigns_pkey" PRIMARY KEY (login, campaignid);


--
-- TOC entry 1945 (class 2606 OID 70764)
-- Name: Clients_pkey; Type: CONSTRAINT; Schema: public; Owner: yadirect; Tablespace: 
--

ALTER TABLE ONLY clients
    ADD CONSTRAINT "Clients_pkey" PRIMARY KEY (login);


--
-- TOC entry 1952 (class 2606 OID 70837)
-- Name: Phrases_pkey; Type: CONSTRAINT; Schema: public; Owner: yadirect; Tablespace: 
--

ALTER TABLE ONLY phrases
    ADD CONSTRAINT "Phrases_pkey" PRIMARY KEY (bannerid, phraseid);


--
-- TOC entry 1954 (class 2606 OID 70876)
-- Name: Statistic_pkey; Type: CONSTRAINT; Schema: public; Owner: yadirect; Tablespace: 
--

ALTER TABLE ONLY statistic
    ADD CONSTRAINT "Statistic_pkey" PRIMARY KEY (campaignid, bannerid, statdate);


--
-- TOC entry 1946 (class 1259 OID 70772)
-- Name: Campaigns_Login_idx; Type: INDEX; Schema: public; Owner: yadirect; Tablespace: 
--

CREATE INDEX "Campaigns_Login_idx" ON campaigns USING btree (login);


--
-- TOC entry 2070 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-04-10 22:56:36 NOVT

--
-- PostgreSQL database dump complete
--

