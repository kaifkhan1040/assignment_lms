from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from app.views import AuthorViewSet,BookViewSet,BorrowRecordViewSet,ReportGenerateView
restricted_router = DefaultRouter()


restricted_router.register('author',AuthorViewSet,basename='authorview')
restricted_router.register('book',BookViewSet,basename='bookview')
restricted_router.register('borrow',BorrowRecordViewSet,basename='borrowview')
# restricted_router.register('reports',ReportGenerateView,basename='reportsview')
