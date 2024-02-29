from tensorflow.keras.preprocessing.image import ImageDataGenerator
training_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_image,
    )

validation_datagen = ImageDataGenerator(preprocessing_function=preprocess_image)

train_generator = training_datagen.flow_from_directory(
    training_dir,
    shuffle=True,
    target_size=(224,224),
    class_mode='categorical',
    batch_size=32
)

validation_generator = validation_datagen.flow_from_directory(
    validating_dir,
    target_size=(224,224),
    shuffle=True,
    class_mode='categorical',
    batch_size=32
)
testing_generator = validation_datagen.flow_from_directory(
    testing_dir,
    target_size=(224,224),
    shuffle=True,
    class_mode='categorical',
    batch_size=32
)
