from django.urls import path, include

from contract import views

urlpatterns = [
    path('latest-contracts/', views.LatestContractsList.as_view()),
    path('contracts/search/', views.search),
    path('contracts/contractsadd/',views.contractAdd),
    path('contracts/participation/',views.participation),
    path('contracts/<slug:smartcontract_slug>/<slug:contract_slug>/', views.ContractDetail.as_view()),
    path('contracts/<slug:smartcontract_slug>/', views.SmartContractDetail.as_view()),
    path('user-contracts/', views.UserContractsList.as_view()),
    path('participation-contracts/', views.UserParticipationList.as_view()),
]