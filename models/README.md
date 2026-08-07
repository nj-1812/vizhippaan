Place these TWO files here:

1. vizhippaan_catboost_model.cbm
2. model_metadata.json

They are created by your final Colab pipeline:

cat_model.save_model('/content/vizhippaan_catboost_model.cbm')

metadata = {
    'features': X.columns.tolist(),
    'categorical': cat_cols
}
