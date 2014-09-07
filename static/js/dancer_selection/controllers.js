var selectionApp = angular.module('selectionApp', []);

selectionApp.directive('bfConfirmClick', [
  function() {
    return {
      link: function(scope, element, attrs) {
        var msg = attrs.bfConfirmClick || "Are you sure?";
        var clickAction = attrs.confirmFunction;
        element.bind('click', function(event) {
          if (window.confirm(msg)) {
            scope.$apply(clickAction)
          }
        });
      }
    };
  }
]);

selectionApp.directive('bfInvisible', [
  function() {
    return {
      link: function(scope, element, attrs) {
        var condition = attrs.bfInvisible;
        var f = attrs.bfInvisibleClick;
        if (scope.$eval(condition)) {
            element.css('visibility', 'hidden');
        }
        else {
             element.bind('click', function(event) {
                scope.$eval(f)
            });
        }
      }
    };
  }
]);


selectionApp.factory('DancerFactory',
    function DancerFactory ($http) {
        _this = DancerFactory;
        _this.dancers = [];
        _this.prefs = [];
        _this.future_prefs = [];

        _this.getPrefs = function(slug, dance_id) {
            return $http.get("/auditions/"+slug+"/prefs/"+dance_id).success(function(response) {
                _this.prefs = response.dancers;
            });
        };

        _this.getDancers = function(slug, dance_id) {
            return $http.get("/auditions/"+slug+"/dancers/"+dance_id).success(function(response) {
                _this.dancers = response.dancers;
              });
        };

        _this.getFuturePrefs = function(slug, dance_id) {
            return $http.get("/auditions/"+slug+"/future_prefs/"+dance_id).success(function(response) {
                _this.future_prefs = response.dancers;
              });
        };

        _this.removeDancerFromList = function(dancer, list) {
            var dancer_index = list.indexOf(dancer);
            list.splice(dancer_index, 1);
        };

        _this.acceptDancer = function(dancer) {
            //call /accept/, append dancer to dancers list
            var data = { 'dancer_id': dancer.dancer_id, 'dance_id': dancer.dance_id };
            var slug = dancer.slug;
            return $http.post('/auditions/'+slug+'/accept_dancer/', data).then(function(response) {
                var data = response.data;
                if (data.successful) {
                    _this.removeDancerFromList(dancer, _this.prefs)
                    _this.dancers.push(dancer);
                }
                return data.successful;
            }, function(response) {
                return false;
            });
        };

        _this.rejectDancer = function(dancer) {
            //remove dancer from list, call /reject/
            var slug = dancer.slug;
            var data = { 'dancer_id': dancer.dancer_id, 'dance_id': dancer.dance_id };
            return $http.post('/auditions/'+slug+'/reject_dancer/', data).then(function(response) {
                var data = response.data;
                if (data.successful) {
                    _this.removeDancerFromList(dancer, _this.prefs)
                }
                return data.successful;
            }, function(response) {
                return false;
            });
        };

        _this.returnDancer = function(dancer) {
            //Remove dancer from list, call /return/
            var slug = dancer.slug;
            var data = { 'dancer_id': dancer.dancer_id, 'dance_id': dancer.dance_id };
            return $http.post('/auditions/'+slug+'/return_dancer/', data).then(function(response) {
                var data = response.data;
                if (data.successful) {
                    _this.removeDancerFromList(dancer, _this.prefs)
                    _this.getFuturePrefs();
                }
                return data.successful;
            }, function(response) {
                return false;
            });
        };

        _this.finishPicking = function(object) {
            //Call /finish/, which rejects remaining dancers
            var data = {'dance_id': object.danceid };
            $http.post('/auditions/'+object.showslug+'/finish/', data).then(function(response) {
                _this.prefs = [];
                _this.future_prefs = [];
                return true;
            }, function(response) {
                return false;
            });
        }
        return _this;
    });

selectionApp.directive('bfcountdown', function($interval) {
    return {
        restrict: 'E',
        link: function($scope, element, attrs) {
            var countDown,
                countingDown;

            $scope.refreshTime = 30;
            $scope.count = "";
            $scope.countdownText = "No preferences left."
            var testAndRefreshPrefs = function() {
                if (countingDown && $scope.count <= 0) {
                    $scope.count = $scope.refreshTime;
                    $scope.refreshPrefs();
                }
            };

            $scope.$watch('count', testAndRefreshPrefs);

            $scope.$watchCollection('future_prefs', function(newValue, oldValue) {
                if ($scope.future_prefs.length == 0 && countingDown) {
                    $scope.countdownText = "No preferences left."
                    $interval.cancel(countDown);
                    $scope.count = "";
                    countingDown = false;
                }
                else if ($scope.future_prefs.length > 0 && !countingDown) {
                    countingDown = true;
                    $scope.countdownText = "Refreshing automatically in:";
                    $scope.count = $scope.refreshTime;
                    countDown = $interval(function() {
                        $scope.count -= 1;
                    }, 1000);
                }
            });
        },
        template: '<span>{{countdownText}} {{count}} </span>'
    };
});


selectionApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';    }
]);

selectionApp.controller('DancerCtrl',
    function DancerCtrl($scope, $http, $timeout, DancerFactory) {

    var slug = $('#show_info').attr("data-slug");
    var dance_id = $('#show_info').attr("data-id");

    $scope.alertIsShown = false;
    $scope.alertText =  "";

    $scope.dancers = DancerFactory.dancers;
    $scope.future_prefs = DancerFactory.future_prefs;
    $scope.prefs = DancerFactory.prefs;

    $scope.showAlert = function(text) {
        $scope.alertIsShown = true;
        $scope.alertText = text;

        $timeout(function() {
            $scope.alertIsShown = false;
        }, 3000);
    };
    $scope.infoAlertIsShown = false;
    $scope.infoAlertText = "";

    $scope.showInfoAlert = function(text) {
        $scope.infoAlertIsShown = true;
        $scope.infoAlertText = text;
        $timeout(function() {
            $scope.infoAlertIsShown = false;
        }, 3000);
    };

    $scope.predicate = "pref"

    $scope.order = function(field) {
        var index = $scope.predicate.indexOf(field);
        if (index === 0) {
            $scope.predicate = '-' + field;
        }
        else {
            $scope.predicate = field;
        }
    };


    $scope.refreshPrefs = function() {
        $scope.count = $scope.refreshTime;
        DancerFactory.getPrefs(slug, dance_id).then(function() {
            $scope.prefs = DancerFactory.prefs;
        });

        DancerFactory.getFuturePrefs(slug, dance_id).then(function() {
            $scope.future_prefs = DancerFactory.future_prefs;
        });
        $scope.showInfoAlert("Refreshed preferences.");
    };


    var makeDecision = function(decisionFunction, action, obj) {
        decisionFunction(obj).then(function(successful) {
            if (successful) {
                $scope.showInfoAlert(action + ' successfully');
            }
            else {
                $scope.showAlert("An error has occurred.");
            }
        });
    };

    $scope.acceptDancer = function(dancer) {
        makeDecision(DancerFactory.acceptDancer, "Accepted dancer", dancer);
    };

    $scope.rejectDancer = function(dancer) {
        makeDecision(DancerFactory.rejectDancer, "Rejected dancer", dancer);
    };

    $scope.returnDancer = function(dancer) {
        makeDecision(DancerFactory.returnDancer, "Returned dancer", dancer);
    };

    $scope.finishPicking = function(danceid, slug) {
        var object = {danceid: dance_id, showslug: slug}
        makeDecision(DancerFactory.finishPicking, "Finished picking", object);
    };

    DancerFactory.getPrefs(slug, dance_id).then(function() {
        $scope.prefs = DancerFactory.prefs;
    });

    DancerFactory.getDancers(slug, dance_id).then(function() {
        $scope.dancers = DancerFactory.dancers;
    });

    DancerFactory.getFuturePrefs(slug, dance_id).then(function() {
        $scope.future_prefs = DancerFactory.future_prefs;
    });
});