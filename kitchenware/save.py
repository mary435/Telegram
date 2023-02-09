import tensorflow as tf

model = tf.keras.models.load_model('xception_v4_larger.h5')
model.save('model')
MODEL = tf.keras.models.load_model('model/')