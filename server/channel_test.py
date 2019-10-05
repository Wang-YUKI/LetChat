from Error import AccessError
import pytest

def auth_register(email, password, name_first, name_last):
    pass

def channel_invite(token, channel_id, u_id):
    pass

def channel_details(token, channel_id):
    pass
def channel_messages(token, channel_id, start):
    pass

def channel_leave(token, channel_id):
    pass

def channel_join(token, channel_id):
    pass

def channel_addowner(token, channel_id, u_id):
    pass

def channel_removeowner(token, channel_id, u_id):
    pass

def channels_list(token):
    pass

def channels_listall(token):
    pass
def channels_create(token, name, is_public):
    pass

def message_send(token, channel_id, message):
    pass

def test_channel_invite_ok():
    
    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")

    channel = channels_create(auth_key_admin["token"], "12345", True)

    channel_invite(auth_key_admin["token"], channel["id"], auth_key["u_id"])
    
    # Check the user is successfully added into channel
    channel_profile = channel_details(auth_key_admin["token"], channel["id"])
    member_list = channel_profile["all_members"]
    assert member_list[0]["u_id"] == auth_key_admin["u_id"]
    assert member_list[1]["u_id"] == auth_key["u_id"]

def test_channel_invite_bad():
 
    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")

    channel = channels_create(auth_key_admin["token"], "12345", True)
    #ValueError
    with pytest.raises(ValueError, match=r"*Channel (based on ID) does not exist*"):
        channel_invite(auth_key_admin["token"], "2222", auth_key["u_id"])

    with pytest.raises(ValueError, match=r"*User is not part of Channel*"):
        channel_invite(auth_key["token"], channel["id"], auth_key_admin["u_id"])

    with pytest.raises(ValueError, match=r"*u_id does not refer to a valid user*"):
        channel_invite(auth_key_admin["token"], channel["id"], "55555")


def test_channel_details_ok():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")

    channel = channels_create("token", "12345", True)

    channel_details(auth_key_admin["token"], channel["id"])

    channel_profile = channel_details(auth_key_admin["token"], channel["id"])
    member_list = channel_profile["all_members"]
    assert member_list[0]["u_id"] == auth_key_admin["u_id"]

def test_channel_details_bad():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")

    channel = channels_create("token", "12345", True)

    #ValueError
    with pytest.raises(ValueError, match=r"*Channel (based on ID) does not exist*"):
        channel_details(auth_key_admin["token"], "123456")

    #AccessError 
    with pytest.raises(AccessError, match=r"*User is not a member of Channel*"):
        channel_details("123456", channel["id"])


def test_channel_messages_ok():

    auth_key = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")

    channel = channels_create(auth_key["token"], "12345", True)
    message_send(auth_key["token"], channel["id"], "testing")

    message_channel = channel_messages(auth_key["token"], channel["id"], 0)
    messages = message_channel["message"]
    assert messages[0]["message"] == "testing"
    assert messages[0]["u_id"] == auth_key["u_id"]


def test_channel_messages_bad():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")

    channel = channels_create(auth_key["token"], "12345", True)

    #ValueError
    with pytest.raises(ValueError, match=r"*Channel (based on ID) does not exis*"):
        channel_messages(auth_key["token"], channel["id"] - 123, 0)

    with pytest.raises(ValueError, match=r"*start is greater than the total number of messages in the channel*"):
        channel_messages(auth_key["token"], channel["id"], 999999999)

    #AccessError 
    with pytest.raises(AccessError, match=r"*User is not a member of Channel*"):
        channel_messages(auth_key_admin["token"], channel["id"], 0)


def test_channel_leave_ok():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    channel = channels_create(auth_key["token"], "12345", True)

    channel_join(auth_key["token"], channel["id"])
    channel_leave(auth_key_admin["token"], channel["id"])

    channel_profile = channel_details(auth_key_admin["token"], channel["id"])
    member_list = channel_profile["all_members"]
    assert member_list[0]["u_id"] == auth_key["u_id"]

def test_channel_leave_bad():

    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    channel = channels_create(auth_key["token"], "12345", True)

    #ValueError
    with pytest.raises(ValueError, match=r"*Channel (based on ID) does not exist*"):
        channel_leave(auth_key["token"], channel["id"] - 123)

def test_channel_join_ok():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    channel = channels_create(auth_key["token"], "12345", True)

    channel_join(auth_key["token"], channel["id"])
    channel_profile = channel_details(auth_key_admin["token"], channel["id"])
    member_list = channel_profile["all_members"]
    assert member_list[0]["u_id"] == auth_key["u_id"]
    assert member_list[1]["u_id"] == auth_key_admin["u_id"]


def test_channel_join_bad():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    channel = channels_create(auth_key_admin["token"], "12345", True)

    #ValueError
    with pytest.raises(ValueError, match=r"*Channel (based on ID) does not exist*"):
        channel_join(auth_key["token"], channel["id"] - 123)

    #AccessError
    channel2 = channels_create("token", "12345", False)
    with pytest.raises(AccessError, match=r"*channel is private*"):
        channel_join(auth_key_admin["token"], channel2["id"])


def test_channel_addowner_ok():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    channel = channels_create(auth_key_admin["token"], "12345", True)

    channel_join(auth_key["token"], channel["id"])

    channel_addowner(auth_key_admin["token"], channel["id"], auth_key["u_id"])
    channel_profile = channel_details(auth_key_admin["token"], channel["id"])
    owner_list = channel_profile["owner_members"]
    assert owner_list[0]["u_id"] == auth_key["u_id"]
    assert owner_list[1]["u_id"] == auth_key_admin["u_id"]


def test_channel_addowner_bad():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key1 = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    auth_key2 = auth_register("123456789adsf@gmail.com", "123456789", "asdfasdff", "asdfcxcxvv")
    auth_key3 = auth_register("123dsf@gmail.com", "123456789", "assdff", "asdfv")
    channel = channels_create(auth_key_admin["token"], "12345", True)

    channel_join(auth_key1["token"], channel["id"])
    channel_join(auth_key2["token"], channel["id"])
    channel_join(auth_key3["token"], channel["id"])
    #ValueError
    with pytest.raises(ValueError, match=r"*Channel (based on ID) does not exist*"):
        channel_addowner(auth_key_admin["token"], channel["id"] - 123, auth_key1["u_id"])

    channel_addowner(auth_key_admin["token"], channel["id"], auth_key1["u_id"])
    with pytest.raises(ValueError, match=r"*User already an owner of the channel*"):
        channel_addowner(auth_key_admin["token"], channel["id"], auth_key1["u_id"])

    #AccessError 
    with pytest.raises(AccessError, match=r"*user is not an owner of the slackr, or an owner of this channel*"):
        channel_addowner(auth_key2["token"], channel["id"], auth_key3["u_id"])


def test_channel_removeowner_ok():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    channel = channels_create(auth_key_admin["token"], "12345", True)

    channel_join(auth_key["token"], channel["id"])

    channel_addowner(auth_key_admin["token"], channel["id"], auth_key["u_id"])
    channel_removeowner(auth_key_admin["token"], channel["id"], auth_key["u_id"])

    channel_profile = channel_details(auth_key_admin["token"], channel["id"])
    owner_list = channel_profile["owner_members"]
    
    if auth_key["u_id"] in owner_list:
        exist = 0
    else:
        exist = 1
    assert exist == 0

    assert owner_list[0]["u_id"] == auth_key_admin["u_id"]

def test_channel_removeowner_bad():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    auth_key1 = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")
    auth_key2 = auth_register("123456789adsf@gmail.com", "123456789", "asdfasdff", "asdfcxcxvv")
    channel = channels_create(auth_key_admin["token"], "12345", True)

    channel_join(auth_key["token"], channel["id"])
    channel_join(auth_key1["token"], channel["id"])
    channel_join(auth_key2["token"], channel["id"])

    channel_addowner(auth_key_admin["token"], channel["id"], auth_key["u_id"])
    #ValueError
    with pytest.raises(ValueError, match=r"*Channel (based on ID) does not exist*"):
        channel_removeowner(auth_key_admin["token"], channel["id"] - 123, auth_key["u_id"])

    with pytest.raises(ValueError, match=r"*User is not an owner of the channel*"):
        channel_removeowner(auth_key_admin["token"], channel["id"], auth_key1["u_id"])

    #AccessError 
    with pytest.raises(AccessError, match=r"*user is not an owner of the slackr, or an owner of this channel*"):
        channel_addowner(auth_key2["token"], channel["id"], auth_key1["u_id"])


def test_channels_list():

    auth_key = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    channel1 = channels_create(auth_key["token"], "12345", True)
    channel2 = channels_create(auth_key["token"], "123asdf45", True)

    channels = channels_list(auth_key["token"])
    assert channels[0]["id"] == channel1["id"]
    assert channels[1]["id"] == channel2["id"]

def test_channels_listall():

    auth_key_admin = auth_register("123456@gmail.com", "123456789", "hhh", "asdf")
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")

    channel1 = channels_create(auth_key["token"], "12345", True)
    channel2 = channels_create(auth_key["token"], "123asdf45", True)
    channels = channels_listall(auth_key_admin["token"])

    assert channels[0]["id"] == channel1["id"]
    assert channels[1]["id"] == channel2["id"]


def test_channels_create_bad():

    #ValueError
    auth_key = auth_register("123456789@gmail.com", "123456789", "asdf", "asdfzcxv")

    with pytest.raises(ValueError, match=r"*Name too long*"):
        channels_create(auth_key["token"], "012345678901234567890123456789", True)