from feeder.backend.omega import OmegaBackend


class AbstractFeederFactory:

    def create(self):
        return OmegaBackend()
