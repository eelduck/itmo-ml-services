-- SQLite
DELETE FROM model;

INSERT INTO model (name, model_path, description, cost)
VALUES ('LGBM', 'models/lgbm.joblib', 'Large model', 15),
       ('Random Forest', 'models/rf.joblib', 'Medium model', 10),
       ('Logistic Regression', 'models/lgbm.joblib', 'Small model', 5);