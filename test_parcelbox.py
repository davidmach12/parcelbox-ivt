from parcelbox import Person, AbstractParcelBox, AbstractNotifier, Parcelbox
from unittest.mock import Mock


def test_hand_in_success() -> None:
    "test ze pri hand_in probehla notifikace odesilatele i prijemce"
    notifier_mock = Mock(spec=AbstractNotifier)
    box = Parcelbox(notifier_mock)
    sender=Person(name = "Pepa Novak", email = "pepa@novak.cz", phone="484455977")
    recipient=Person(name="Jan Svoboda", email="jan@svoboda.cz", phone="456123789")
    balik = box.hand_in(sender=sender,recipient=recipient)
    notifier_mock.notifikuj.assert_any_call(sender,f"Pepa Novak, Balik {balik.id} (None) je odeslán. Pin je {balik.pin}.")
    notifier_mock.notifikuj.assert_any_call(recipient,f"Jan Svoboda, Balik {balik.id} (None) prisel. Pin je {balik.pin}.")


def test_hand_out_success() -> None:
    "test ze pri hand_out probehla notifikace odesilatele o vyzvednute zasilce"
    notifier_mock = Mock(spec=AbstractNotifier)
    box = Parcelbox(notifier_mock)
    sender=Person(name = "Pepa Novak", email = "pepa@novak.cz", phone="484455977")
    recipient=Person(name="Jan Svoboda", email="jan@svoboda.cz", phone="456123789")
    balik = box.hand_in(sender=sender,recipient=recipient)
    assert box.hand_out(balik.id, balik.pin, sender) == balik
    notifier_mock.notifikuj.assert_any_call(sender,f"Pepa Novak, Balík {balik.id} (None) byl vyzvednut.")

def test_fail_handout_bad_id() -> None:
    "test ze pri hand_out a nespravnem id nevratil parcelbox nic/vratil None"
    notifier_mock = Mock(spec=AbstractNotifier)
    box = Parcelbox(notifier_mock)
    sender=Person(name = "Pepa Novak", email = "pepa@novak.cz", phone="484455977")
    recipient=Person(name="Jan Svoboda", email="jan@svoboda.cz", phone="456123789")
    balik = box.hand_in(sender=sender,recipient=recipient)
    assert box.hand_out("bad_id", balik.pin, sender) is None

def test_fail_handout_bad_pin() -> None:
    ...
    "test ze pri hand_out a spravnem id a nespravnem pinu nevratil parcelbox nic/vratil None"
    notifier_mock = Mock(spec=AbstractNotifier)
    box = Parcelbox(notifier_mock)
    sender=Person(name = "Pepa Novak", email = "pepa@novak.cz", phone="484455977")
    recipient=Person(name="Jan Svoboda", email="jan@svoboda.cz", phone="456123789")
    balik = box.hand_in(sender=sender,recipient=recipient)
    assert box.hand_out(balik.id, "bad_pin", sender) is None
 
 
 
test_hand_in_success()
test_fail_handout_bad_id()
test_fail_handout_bad_pin()