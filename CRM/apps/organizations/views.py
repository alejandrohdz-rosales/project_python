from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .permissions import CanManageOrganization, IsOrganizationMember, IsSuperuser
from .serializers import OrganizationSerializer
from .tenancy import organizations_for_user


class OrganizationListCreate(ListCreateAPIView):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return organizations_for_user(self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsSuperuser()]
        return [IsOrganizationMember()]


class OrganizationDetail(RetrieveUpdateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [CanManageOrganization]

    def get_queryset(self):
        return organizations_for_user(self.request.user)
