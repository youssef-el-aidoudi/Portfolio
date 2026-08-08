from tensorflow import keras
from data_loader import load_datasets
from config import MODEL_PATH

def main():
    _, _, test_ds, class_names = load_datasets()
    print("Classes:", class_names)

    model = keras.models.load_model(MODEL_PATH)
    test_loss, test_acc = model.evaluate(test_ds)

    print("Evaluation finished")
    print("Test loss:", test_loss)
    print("Test accuracy:", test_acc)

if __name__ == "__main__":
    main()
