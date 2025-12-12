# app.py
# TODO: importer FastAPI
from fastapi import FastAPI
from feast import FeatureStore

# TODO: créer une instance FastAPI
app = FastAPI()

# TODO: définir une route GET /health
@app.get("/health")
def health():
    return {"status": "ok"}

store = FeatureStore(repo_path="/repo")


@app.get("/features/{user_id}")
def get_features(user_id: str):
    features = [
        "subs_profile_fv:months_active",
        "subs_profile_fv:monthly_fee",
        "subs_profile_fv:paperless_billing",
    ]

    feature_dict = store.get_online_features(
        features=features,
        entity_rows=[{"user_id": user_id}],
    ).to_dict()

    # On convertit en format plus simple (clé -> valeur scalaires)
    simple = {name: values[0] for name, values in feature_dict.items()}

    return {
        "user_id": user_id,
        "features": simple,
    }