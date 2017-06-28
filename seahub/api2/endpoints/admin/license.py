# Copyright (c) 2012-2016 Seafile Ltd.
import os
import logging

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from seahub.api2.authentication import TokenAuthentication
from seahub.api2.throttling import UserRateThrottle
from seahub.api2.utils import api_error
from seahub.settings import LICENSE_PATH

logger = logging.getLogger(__name__)


class AdminLicense(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    throttle_classes = (UserRateThrottle, )
    permission_classes = (IsAdminUser,)

    def post(self, request):
        license_file = request.FILES.get('license', None)
        if not license_file:
            error_msg = 'license invalid.'
            return api_error(status.HTTP_400_BAD_REQUEST, error_msg)

        license_dir = os.path.dirname(LICENSE_PATH)
        try:
            if not os.path.exists(license_dir):
                error_msg = 'path %s invalid.'% LICENSE_PATH
                return api_error(status.HTTP_400_BAD_REQUEST, error_msg)

            with open(LICENSE_PATH, 'w') as fd:
                fd.write(license_file.read())
        except Exception as e:
            logger.error(e)
            return api_error(status.HTTP_500_INTERNAL_SERVER_ERROR, error_msg)
        return Response({'success': True}, status=status.HTTP_200_OK)
