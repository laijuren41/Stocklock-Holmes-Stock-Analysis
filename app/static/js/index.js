var app = angular.module('stockAn', []);

app.controller('stockAnController', function($scope, $http) {

	//$scope.stockList = [{stockText: 'Stock1'}];

	$http.get('/api/stock/data/').then(function(response) {
		$scope.stockList = [];

		/*
		for(var i = 0; i < response.data.length; i++) {


		}
		*/

		console.log(response.data);
	});

	$scope.saveData = function() {

		var data = {}
		$.http.put('/api/stock/data/')
	}


	$scope.stockAdd = function() {

		$scope.stockList.push({stockText: $scope.stockInput});
		$scope.stockInput = '';
	}

})
