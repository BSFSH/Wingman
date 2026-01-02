from Wingman.gui.app import XPTrackerApp
from Wingman.core.session import GameSession
from Wingman.core.input_receiver import InputReceiver

class TestApp():
    def test_update_gui(self):
        receiver = InputReceiver()
        session = GameSession(receiver)
        app = XPTrackerApp(session)
        receiver.receive("""Beautiful's group:

[ Class        Lvl] Status     Name                 Hits               Fat                Power            
[Sin            69]           Beautiful            500/ 500 (100%)    497/ 500 ( 99%)    592/ 707 ( 83%)   
[Skelton        50]           Skeletor             396/ 396 (100%)    396/ 396 (100%)    554/ 554 (100%) """)
        app.update_gui()
        groupCountBeforeNewFollower = len(app.tree.get_children())

        receiver.receive("FooBar follows you")
        app.update_gui()
        groupCountAfterNewFollower = len(app.tree.get_children())

        assert groupCountAfterNewFollower == groupCountBeforeNewFollower + 1
        assert groupCountAfterNewFollower == 3