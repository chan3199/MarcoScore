import tensorflow as tf

model = tf.keras.models.load_model("model/model_long.h5")
print("model_long : ")
print(model.input_shape)
model2 = tf.keras.models.load_model("model/model_recent.h5")
print("model_recent : ")
print(model2.input_shape)

