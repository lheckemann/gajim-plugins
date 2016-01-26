# -*- coding: utf-8 -*-
#
# Copyright 2015 Tarek Galal <tare2.galal@gmail.com>
#
# This file is part of Gajim-OMEMO plugin.
#
# The Gajim-OMEMO plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Gajim-OMEMO is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# the Gajim-OMEMO plugin.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import sqlite3

from axolotl.state.axolotlstore import AxolotlStore
from axolotl.util.keyhelper import KeyHelper

from .liteidentitykeystore import LiteIdentityKeyStore
from .liteprekeystore import LitePreKeyStore
from .litesessionstore import LiteSessionStore
from .litesignedprekeystore import LiteSignedPreKeyStore
from .encryption import EncryptionState

log = logging.getLogger('gajim.plugin_system.omemo')

DEFAULT_PREKEY_AMOUNT = 100


class LiteAxolotlStore(AxolotlStore):
    def __init__(self, db):
        log.debug('Opening the DB ' + str(db))
        conn = sqlite3.connect(db, check_same_thread=False)
        conn.text_factory = bytes
        self.identityKeyStore = LiteIdentityKeyStore(conn)
        self.preKeyStore = LitePreKeyStore(conn)
        self.signedPreKeyStore = LiteSignedPreKeyStore(conn)
        self.sessionStore = LiteSessionStore(conn)
        self.encryptionStore = EncryptionState(conn)

        if not self.getLocalRegistrationId():
            log.info("Generating Axolotl keys for db" + str(db))
            self._generate_axolotl_keys()

    def _generate_axolotl_keys(self):
        identityKeyPair = KeyHelper.generateIdentityKeyPair()
        registrationId = KeyHelper.generateRegistrationId()
        preKeys = KeyHelper.generatePreKeys(KeyHelper.getRandomSequence(),
                                            DEFAULT_PREKEY_AMOUNT)
        self.storeLocalData(registrationId, identityKeyPair)

        for preKey in preKeys:
            self.storePreKey(preKey.getId(), preKey)

    def getIdentityKeyPair(self):
        return self.identityKeyStore.getIdentityKeyPair()

    def storeLocalData(self, registrationId, identityKeyPair):
        self.identityKeyStore.storeLocalData(registrationId, identityKeyPair)

    def getLocalRegistrationId(self):
        return self.identityKeyStore.getLocalRegistrationId()

    def saveIdentity(self, recepientId, identityKey):
        self.identityKeyStore.saveIdentity(recepientId, identityKey)

    def isTrustedIdentity(self, recepientId, identityKey):
        return self.identityKeyStore.isTrustedIdentity(recepientId,
                                                       identityKey)

    def loadPreKey(self, preKeyId):
        return self.preKeyStore.loadPreKey(preKeyId)

    def loadPreKeys(self):
        return self.preKeyStore.loadPendingPreKeys()

    def storePreKey(self, preKeyId, preKeyRecord):
        self.preKeyStore.storePreKey(preKeyId, preKeyRecord)

    def containsPreKey(self, preKeyId):
        return self.preKeyStore.containsPreKey(preKeyId)

    def removePreKey(self, preKeyId):
        self.preKeyStore.removePreKey(preKeyId)

    def loadSession(self, recepientId, deviceId):
        return self.sessionStore.loadSession(recepientId, deviceId)

    def getSubDeviceSessions(self, recepientId):
        return self.sessionStore.getSubDeviceSessions(recepientId)

    def storeSession(self, recepientId, deviceId, sessionRecord):
        self.sessionStore.storeSession(recepientId, deviceId, sessionRecord)

    def containsSession(self, recepientId, deviceId):
        return self.sessionStore.containsSession(recepientId, deviceId)

    def deleteSession(self, recepientId, deviceId):
        self.sessionStore.deleteSession(recepientId, deviceId)

    def deleteAllSessions(self, recepientId):
        self.sessionStore.deleteAllSessions(recepientId)

    def loadSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.loadSignedPreKey(signedPreKeyId)

    def loadSignedPreKeys(self):
        return self.signedPreKeyStore.loadSignedPreKeys()

    def storeSignedPreKey(self, signedPreKeyId, signedPreKeyRecord):
        self.signedPreKeyStore.storeSignedPreKey(signedPreKeyId,
                                                 signedPreKeyRecord)

    def containsSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.containsSignedPreKey(signedPreKeyId)

    def removeSignedPreKey(self, signedPreKeyId):
        self.signedPreKeyStore.removeSignedPreKey(signedPreKeyId)
