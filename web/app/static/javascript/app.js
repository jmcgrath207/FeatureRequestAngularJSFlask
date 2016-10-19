
var app = angular.module('myApp', ['ui.grid']);


app.service('sharedModels', [function () {

    'use strict';


    // Shared Models
    this.data = [];

}]);


//Define a custom filter to search only visible columns (used with grid 3)
app.filter('visibleColumns', function() {
  return function(data, grid, query) {

    matches = [];

    //no filter defined so bail
    if (query === undefined|| query==='') {
      return data;
    }

    query = query.toLowerCase();

    //loop through data items and visible fields searching for match
    for (var i = 0; i < data.length; i++) {
      for (var j = 0; j < grid.columnDefs.length; j++) {

        var dataItem = data[i];
        var fieldName = grid.columnDefs[j]['field'];

        //as soon as search term is found, add to match and move to next dataItem
        if (dataItem[fieldName].toString().toLowerCase().indexOf(query)>-1) {
          matches.push(dataItem);
          break;
        }
      }
    }
    return matches;
  }
});

//Setup the Controller
app.controller('caseview', function($scope, $filter, $http,$window,sharedModels) {

    /* TODO: Add sample data to scope */

    $scope.clientid_url = $window.clientid_url;

        $http.get($scope.clientid_url)
       .then(function(res){
          $scope.Data = res.data;
         });

    $scope.Data =  sharedModels.data;

  $scope.filterText;

  $scope.filterGrid1 = {};


  $scope.refreshData = function() {
      $scope.filterGrid1.data = $filter('filter')($scope.Data, $scope.filterText, undefined);

  };
});

app.controller("caseform", ['$scope', '$http','$window',  function($scope, $http,$window) {
$scope.addRowAsyncAsJSON = function(){

            $scope.clientid_url = $window.clientid_url;


          /* TODO: find out how to push data to other scope without page refresh */
          /*  shareddata.Data.push({
            case_name : $scope.case_name,
            client_id : $scope.client_id,
            description : $scope.description,
            priority : $scope.priority,
            product_area : $scope.product_area,
            target_date : $scope.target_date
            }); */



		// Writing it to the server
		//
		var dataObj = {
				case_name : $scope.case_name,
				description : $scope.description,
                priority : parseInt($scope.priority),
                product_area : $scope.product_area,
                target_date : $scope.target_date
		};

		var res = $http.post($scope.clientid_url, dataObj);
		res.success(function(data, status, headers, config) {
			$scope.message = data;
		});
		// Making the fields empty
		//
        /* $scope.case_name='';
        $scope.client_id='';
        $scope.description='';
        $scope.priority='';
        $scope.product_area='';
        $scope.target_date=''; */

	};
}]);