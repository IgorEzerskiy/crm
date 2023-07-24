from django.urls import path

from crm_app.views import OrderListView, UserLoginView, UserLogoutView, UserCreateView, ClientCreateView, \
    ClientListView, ClientUpdateView, CompanyUpdateView, UserListView, UserDetailView, UserConnectionRequestsListView, \
    OrderCreateView, CommentCreateView, OrderUpdateView, ProfileInfoUpdateView

urlpatterns = [
    path('board/', OrderListView.as_view(), name='board'),
    path('', OrderListView.as_view(), name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('new_client/', ClientCreateView.as_view(), name='new_client'),
    path('edit_client/<int:pk>', ClientUpdateView.as_view(), name='edit_client'),
    path('edit_company/<int:pk>', CompanyUpdateView.as_view(), name='edit_company'),
    path('users/', UserListView.as_view(), name='users'),
    path('users-connections-requests/', UserConnectionRequestsListView.as_view(), name='users_connections_requests'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('new_order/', OrderCreateView.as_view(), name='new_order'),
    path('add-comment/', CommentCreateView.as_view(), name='add_comment'),
    path('update-order/<int:pk>', OrderUpdateView.as_view(), name='update_order'),
    path('update-profile/<int:pk>', ProfileInfoUpdateView.as_view(), name='update_profile'),
]
