from config import EPOCHS, MODEL_PATH
from data_loader import load_datasets
from model import build_model
from utils import ensure_dir, save_class_names

def main():
    train_ds, val_ds, test_ds, class_names = load_datasets()
    print("Classes:", class_names)

    model = build_model()
    model.summary()

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS
    )

    test_loss, test_acc = model.evaluate(test_ds)
    print("Test accuracy:", test_acc)

    ensure_dir("models")
    model.save(MODEL_PATH)
    save_class_names(class_names)

    print(f"Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
