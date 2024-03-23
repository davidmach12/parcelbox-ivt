
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from util import random_pin
import uuid


@dataclass
class Person:
    # jmeno a prijmeni dohromady
    name: str
    phone: str
    email: str


@dataclass
class Parcel:
    id: str
    pin: str
    description: Optional[str]
    sender: Person
    recipient: Person


class AbstractParcelBox(ABC):

    @abstractmethod
    def hand_in(self, sender: Person, recipient: Person, description: Optional[str] = None) -> Parcel:
        '''
        Prebira zasilku/balicek od odesilatele, notifikuje jak odesilatele tak prijemce.
        :param sender: odesilatel, tomu se zasila potvrzeni
        :param recipient: prijemce, tomu se zasila vyzva k vyzvednuti
        :param description: volitelny popisek balicku
        :returns: reprezentace prevzateho balicku (s vygenerovanym id a pin)
        '''

    @abstractmethod
    def hand_out(self, id: str, pin: str, sender: Person) -> Optional[Parcel]:
        '''
        Vydava zasilku, notifikuje odesilatele o jejim vydani.
        :param id: id zasilky (z notifikace/vyzvy k vyzvednuti)
        :param pin: PIN k vyzvednuti
        :returns: reprezentace vydaneho balicku, nebo None v pripade ze balicek neexistuje nebo PIN nesedi
        '''


class AbstractNotifier(ABC):
    @abstractmethod
    def notifikuj(self, recipient: Person, text: str) -> None:
        ...


class Parcelbox(AbstractParcelBox):

    def __init__(self, notifier: AbstractNotifier):
        self.notifier = notifier
        self.store: dict[str,Parcel] = {}

    def hand_in(self, sender: Person, recipient: Person, description: Optional[str] = None) -> Parcel:
        id = str(uuid.uuid4())
        pin = random_pin()
        p=Parcel(id=id,description= description, sender=sender, recipient=recipient, pin=pin)
        self.store.update({id:p})
        self.notifier.notifikuj(sender, f"{sender.name}, Balik {id} ({p.description}) je odeslán. Pin je {pin}.")
        self.notifier.notifikuj(recipient, f"{recipient.name}, Balik {id} ({p.description}) prisel. Pin je {pin}.")
        return p

    def hand_out(self, id: str, pin: str, sender: Person) -> Optional[Parcel]:
        if id not in self.store:
            return None
        p = self.store[id]
        if p.pin == pin:
            self.notifier.notifikuj(sender, f"{sender.name}, Balik {id} ({p.description}) byl vyzvednut.")
            return p
        else:
            return None
        

class Notifier(AbstractNotifier):
    def notifikuj(self, recipient: Person, text: str) -> None:
        print(f'Komu: {recipient.email} ')
        print(text)
        return


    # dobrovolne rozsireni: vydani pouze dle PINu
    #@abstractmethod
    #def vydej_zasilku_dle_pin(self, pin: str) -> Optional[Zasilka]:
        #...


# doplnte zde jeste kontrakt pro notifikator, napr. AbstractNotifier, ktery bude umet zasilat text oznameni na danou mailovou adresu
# tento notifikator bude uvnitr pouzivat vase implementace AbstractParcelBoxu
# implementace AbstractNotifier bude jen vypisovat co posila a kam to posila pomoci print