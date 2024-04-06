import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.layers import BatchNormalization

# Create a BatchNormalization layer
batch_norm_layer = BatchNormalization()

# # Use the layer in your model
# model = tf.keras.Sequential([
#     layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
#     batch_norm_layer,
#     layers.MaxPooling2D((2, 2)),
#     # ... other layers ...
# ])

# # Compile and train your model as usual
# model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
# # ... (training data) ...
# model.fit(x_train, y_train, epochs=5)