#Area para pruebas

import tensorflow as tf
from tensorflow.keras import layers

# Load the dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

# Normalize the data
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

# Define the model
model = tf.keras.Sequential([
  layers.Conv2D(64, (3,3), padding='same', activation='relu'),
  layers.BatchNormalization(),
  layers.Conv2D(64, (3,3), padding='same', activation='relu'),
  layers.BatchNormalization(),
  layers.Conv2D(64, (3,3), padding='same', activation='relu'),
  layers.BatchNormalization(),
  layers.Conv2D(64, (3,3), padding='same', activation='relu'),
  layers.BatchNormalization(),
  layers.Conv2D(3, (1,1), padding='same')
])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
print("entrenando")
model.fit(x_train, x_train, epochs=10, batch_size=32, validation_data=(x_test, x_test))
print("entrenado")

# Generate new images using the model
generated_images = model.predict(x_test[:10])
print(generated_images)