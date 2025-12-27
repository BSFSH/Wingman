import threading
from XPTracker.core.input_receiver import InputReceiver
from XPTracker.core.session import GameSession
from XPTracker.core.network_listener import NetworkListener
from XPTracker.gui.app import XPTrackerApp

if __name__ == "__main__":
    # Create the SHARED receiver
    shared_receiver = InputReceiver()

    # Pass it to both
    listener = NetworkListener(shared_receiver)
    session = GameSession(shared_receiver)

    # Start app
    app = XPTrackerApp(session)
    listener.start()
    app.run()