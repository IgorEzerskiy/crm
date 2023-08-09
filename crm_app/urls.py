from django.urls import path
from django.conf.urls.static import static
from crm_app.views import OrderListView, UserLoginView, UserLogoutView, UserCreateView, ClientCreateView, \
    ClientListView, ClientUpdateView, CompanyUpdateView, UserListView, UserDetailView, UserConnectionRequestsListView, \
    OrderCreateView, CommentCreateView, OrderUpdateView, ClientDeleteView, ProfileInfoUpdateView, PasswordUpdateView, \
    ClientRecoveryUpdateView, UsersUpdateView, UserDeleteView, UserConnectionApproveView, UserConnectionDeleteView
from CRM import settings

urlpatterns = [
    path('board/', OrderListView.as_view(), name='board'),
    path('', OrderListView.as_view(), name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('new-client/', ClientCreateView.as_view(), name='new_client'),
    path('edit-client/<int:pk>', ClientUpdateView.as_view(), name='edit_client'),
    path('edit-company/<int:pk>', CompanyUpdateView.as_view(), name='edit_company'),
    path('users/', UserListView.as_view(), name='users'),
    path('user-connection-requests/', UserConnectionRequestsListView.as_view(), name='users_connections_requests'),
    path('approve-user-connetcion/<int:pk>', UserConnectionApproveView.as_view(), name='approve_user_connection'),
    path('cancel-user-connection/<int:pk>', UserConnectionDeleteView.as_view(), name='cancel_user_connection'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('new-order/', OrderCreateView.as_view(), name='new_order'),
    path('add-comment/', CommentCreateView.as_view(), name='add_comment'),
    path('update-order/<int:pk>', OrderUpdateView.as_view(), name='update_order'),
    path('client-delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('update-profile/<int:pk>', ProfileInfoUpdateView.as_view(), name='update_profile'),
    path('change-password/<int:pk>', PasswordUpdateView.as_view(), name='change_password'),
    path('recovery-client/<int:pk>', ClientRecoveryUpdateView.as_view(), name='recovery_client'),
    path('update-users/<int:pk>', UsersUpdateView.as_view(), name='update_users'),
    path('user-delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
              ] \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
