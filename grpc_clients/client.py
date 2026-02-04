import grpc
from grpc_clients.gen import remna_pb2_grpc
from grpc_clients.gen.remna_pb2 import (
    EmptyRequest,
    PingResponse,
    GetUserByUsernameRequest,
    GetUserByTgIDRequest,
    GetUserByEmailRequest,
    CreateUserRequest,
    UserResponse,
    UpdateUserRequest,
    MultipleUsersResponse,
    GetUserUUIDRequest
)

class RemnaClient:
    def __init__(self, stub_url: str):
        channel = grpc.insecure_channel(stub_url)
        self.stub = remna_pb2_grpc.RemnaServiceStub(channel)

    def create_user(self, plan: str, username: str="", email: str="", tgid: str=""):
        request = CreateUserRequest(username=username, email=email, tgid=tgid, plan=plan)
        return self.stub.CreateUser(request)

    def get_user_by_username(self, username: str):
        request = GetUserByUsernameRequest(username=username)
        return self.stub.GetUser(request)

    def get_users_by_email(self, email: str):
        request = GetUserByEmailRequest(email=email)
        return self.stub.GetUsersByEmail(request)

    def update_user_expiry_time(self, plan: str, username: str="", uuid: str=""):
        request = UpdateUserRequest(username=username, uuid=uuid, plan=plan)
        return self.stub.UpdateUserExpiryTime(request)

    def get_user_hwid_devices(self, uuid: str):
        request = GetUserUUIDRequest(uuid=uuid)
        return self.stub.GetUserHwidDevices(request)

    def get_srh_history(self):
        request = EmptyRequest()
        return self.stub.GetSRHHistory(request)
    
    def get_users(self):
        request = EmptyRequest()
        return self.stub.GetAllUsers(request)
    