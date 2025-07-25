import logging
from datetime import datetime

import requests
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin.auth import verify_id_token
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from leaderboard.models import (
    LeetcodeUser,
    User,
    UserNames,
    codechefUser,
    codeforcesUser,
    githubUser,
    openlakeContributor,
)

from .firebase import default_app

logger = logging.getLogger(__name__)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def getRoutes(request):
    routes = ["/api/token", "api/token/refresh"]
    return Response(routes)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user
    return Response(
        {
            "username": user.username,
            "email": user.email,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def post_UserNames(request):
    try:
        username_cc = request.data.get("cc_uname", "")
        username_cf = request.data.get("cf_uname", "")
        username_gh = request.data.get("gh_uname", "")
        username_lt = request.data.get("lt_uname", "")
        user = request.user

        with transaction.atomic():
            # Check if user already exists in UserNames
            t = UserNames.objects.filter(user=user).first()

            if t:
                # Update and delete only if the value changes
                if username_cc and t.cc_uname != username_cc:
                    codechefUser.objects.filter(username=t.cc_uname).delete()
                    t.cc_uname = username_cc
                    codechefUser.objects.get_or_create(username=username_cc)

                if username_cf and t.cf_uname != username_cf:
                    codeforcesUser.objects.filter(username=t.cf_uname).delete()
                    t.cf_uname = username_cf
                    codeforcesUser.objects.get_or_create(username=username_cf)

                if username_gh and t.gh_uname != username_gh:
                    githubUser.objects.filter(username=t.gh_uname).delete()
                    t.gh_uname = username_gh
                    githubUser.objects.get_or_create(username=username_gh)

                if username_lt and t.lt_uname != username_lt:
                    LeetcodeUser.objects.filter(username=t.lt_uname).delete()
                    t.lt_uname = username_lt
                    LeetcodeUser.objects.get_or_create(username=username_lt)

                t.save()

            else:
                # Create new UserNames entry
                userName = UserNames(
                    user=user,
                    cc_uname=username_cc,
                    cf_uname=username_cf,
                    gh_uname=username_gh,
                    lt_uname=username_lt,
                )
                userName.save()

                # Create corresponding user entries
                if username_cc:
                    codechefUser.objects.get_or_create(username=username_cc)
                if username_cf:
                    codeforcesUser.objects.get_or_create(username=username_cf)
                if username_gh:
                    githubUser.objects.get_or_create(username=username_gh)
                if username_lt:
                    LeetcodeUser.objects.get_or_create(username=username_lt)

        return Response(
            {
                "status": 200,
                "message": "Success",
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {
                "status": 400,
                "message": str(e),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def registerUser(request):
    logger.info("Received a request to register a user")

    try:
        # Log incoming data
        logger.debug(f"Request data: {request.data}")

        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        email = request.data.get("email", "")
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        cc_uname = request.data.get("cc_uname", "")
        cf_uname = request.data.get("cf_uname", "")
        gh_uname = request.data.get("gh_uname", "")
        lt_uname = request.data.get("lt_uname", "")

        if not all([first_name, email, username]):
            logger.error("Missing required fields: first_name, email, username")
            return Response(
                {"status": 400, "message": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.save()
        logger.info(f"User {username} created successfully")

        # Save usernames
        userName = UserNames(
            user=user,
            cc_uname=cc_uname,
            cf_uname=cf_uname,
            gh_uname=gh_uname,
            lt_uname=lt_uname,
        )
        userName.save()
        logger.info(f"Usernames for {username} saved successfully")

        # Save platform-specific usernames
        if cc_uname:
            cc_user = codechefUser(username=cc_uname)
            cc_user.save()
            logger.info(f"CodeChef username {cc_uname} saved")
        if cf_uname:
            cf_user = codeforcesUser(username=cf_uname)
            cf_user.save()
            logger.info(f"Codeforces username {cf_uname} saved")
        if gh_uname:
            gh_user = githubUser(username=gh_uname)
            gh_user.save()
            logger.info(f"GitHub username {gh_uname} saved")
        if lt_uname:
            lt_user = LeetcodeUser(username=lt_uname)
            lt_user.save()
            logger.info(f"LeetCode username {lt_uname} saved")

        return Response(
            {
                "status": 200,
                "message": "Success",
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("An error occurred while registering the user")
        return Response(
            {"status": 400, "message": "An error occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def loginGoogleUser(request):
    try:
        token = request.data.get("token", "")
        verified = verify_id_token(token, default_app)

        uid = verified.get("uid")
        user = User.objects.get(uid=uid)

        refresh = RefreshToken.for_user(user)
        token = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(
            {
                "status": 200,
                "message": "Success",
                "token": token,
            },
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response(
            {"status": 400, "message": "Please sign up before logging in"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.exception("An error occurred while logging in")
        return Response(
            {"status": 400, "message": "An error occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def registerGoogleUser(request):
    logger.info("Received a request to register a user")

    try:
        # Log incoming data
        logger.debug(f"Request data: {request.data}")

        token = request.data.get("token", "")
        verified = verify_id_token(token, default_app)
        name = verified["name"].split(" ")
        first_name = name[0]
        if len(name) >= 2:
            last_name = name[-1]
        else:
            last_name = ""
        email = verified.get("email", "")
        uid = verified.get("uid")
        username = request.data.get("username", "")

        if not all([first_name, email, username]):
            logger.error("Missing required fields: first_name, email, username")
            return Response(
                {"status": 400, "message": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create user
        user = User.objects.create_user(
            uid=uid,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_unusable_password()
        user.save()
        logger.info(f"User {username} created successfully")

        # Create a token manually as user is not made using the normal authentication method
        refresh = RefreshToken.for_user(user)
        token = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(
            {
                "status": 200,
                "message": "Success",
                "token": token,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.exception("An error occurred while registering the user")
        return Response(
            {"status": 400, "message": "An error occurred"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# def get_ranking(contest, usernames):
#     API_URL_FMT = 'https://leetcode.com/contest/api/ranking/{}/?pagination={}&region=global'
#     page = 1
#     total_rank = []
#     retry_cnt = 0

#     while retry_cnt<10:
#         try:

#             url = API_URL_FMT.format(contest, page)
#             # if page == 3 :
#             #     break
#             resp = requests.get(url).json()
#             page_rank = resp['total_rank']
#             if len(page_rank) == 0:
#                 break
#             total_rank.extend(page_rank)
#             print(f'Retrieved ranking from page {page}. {len(total_rank)} retrieved.')

#             # logger.info(f'Retrieved ranking from page {page}. {len(total_rank)} retrieved.')
#             page += 1
#             if(page==3):
#                 break
#             retry_cnt = 0
#         except:
#             print(f'Failed to retrieve data of page {page}...retry...{retry_cnt}')
#             retry_cnt += 1

#     # Discard and transform fields
#     for rank in total_rank:
#         rank.pop('contest_id', None)
#         rank.pop('user_slug', None)
#         rank.pop('country_code', None)
#         rank.pop('global_ranking', None)
#         finish_timestamp = rank.pop('finish_time', None)
#         if finish_timestamp:
#             rank['finish_time'] = datetime.fromtimestamp(int(finish_timestamp)).isoformat()

#     # Filter rankings based on usernames

#     filtered_rankings = [rank for rank in total_rank if rank['username'] in usernames]

#     filtered_rankings.sort(key=lambda obj: obj["rank"])

#     return filtered_rankings


import urllib.parse

import requests


def get_data_from_url(usernames, contestID):
    base_url = "https://leetcode.com/graphql"
    data_list = []
    contest_data = []

    for username in usernames:
        # Construct the query parameters
        query = f'query {{ userContestRankingHistory(username:"{username}") {{ attended ranking contest {{ title startTime }} }} }}'
        query_params = {"query": query}

        # Encode the query parameters
        encoded_params = urllib.parse.urlencode(query_params)

        # Construct the full URL with the encoded query parameters
        url = f"{base_url}?{encoded_params}"

        try:
            response = requests.get(url)
            data = response.json()

            # Process the retrieved data as per your requirements

            data_object = {"username": username, "data": data}
            data_list.append(data_object)

        except requests.exceptions.RequestException as e:
            # Handle any errors that occurred during the request
            print(f"Error: {e}")

    for item in data_list:
        username = item["username"]
        user_data = item["data"]["data"]["userContestRankingHistory"]

        if user_data is not None:
            for contest in user_data:
                if contest["contest"]["title"] == contestID:
                    contest_info = {
                        "username": username,
                        "ranking": contest["ranking"],
                        "startTime": contest["contest"]["startTime"],
                    }
                    contest_data.append(contest_info)
    sorted_contest_data = sorted(contest_data, key=lambda x: x["ranking"], reverse=True)

    return sorted_contest_data


def ContestRankingsAPIView(request):

    if request.method == "GET":
        contest = request.GET.get("contest")

        usernames = [user.username for user in LeetcodeUser.objects.all()]

        task = get_data_from_url(usernames, contest)

    return JsonResponse(task, safe=False)
