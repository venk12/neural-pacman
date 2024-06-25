class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.value = None
            cls._instance.baseline_value = None
            cls._instance.psd = None
        return cls._instance