CREATE OR REPLACE VIEW vw_gazetteer_c5000_tng AS
 SELECT vw_gazetteer_tng.id, vw_gazetteer_tng.name, vw_gazetteer_tng.lang, vw_gazetteer_tng.longitude, vw_gazetteer_tng.latitude, vw_gazetteer_tng.altitude, vw_gazetteer_tng.population, vw_gazetteer_tng.country_code, vw_gazetteer_tng.feature_class, vw_gazetteer_tng.feature_code, vw_gazetteer_tng.parent, vw_gazetteer_tng.preferred, vw_gazetteer_tng.short
   FROM vw_gazetteer_tng
     WHERE vw_gazetteer_tng.population >= 5000 AND ((short = TRUE OR lang = ANY (ARRAY['en'::bpchar, ''::bpchar])) OR lang IS NULL);


CREATE OR REPLACE VIEW vw_gazetteer_tng AS 
SELECT gazetteerentity.id, gazetteerentry.name, gazetteerentry.lang, gazetteerentity.longitude, gazetteerentity.latitude, gazetteerentity.altitude, gazetteerentity.population, gazetteerentity.country_code, gazetteerentity.feature_class, gazetteerentity.feature_code, locatedin.parent_id AS parent, gazetteerentry.ispreferredname AS preferred , gazetteerentry.isshortname AS short
   FROM gazetteerentity
      JOIN hasname ON hasname.entity_id = gazetteerentity.id
      JOIN gazetteerentry ON hasname.entry_id = gazetteerentry.id
      LEFT JOIN locatedin ON locatedin.child_id = gazetteerentity.id
      WHERE gazetteerentry.isambigious = false;
