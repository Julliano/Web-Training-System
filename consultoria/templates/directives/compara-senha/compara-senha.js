(function() {
	"use sctrict";

	angular.module("consultoria").directive("comparaSenha", comparaSenha);

	function comparaSenha() {
		return {
			require : "ngModel",
			scope : {
				comparaCom : "="
			},
			link : function(scope, element, attributes, ngModel) {

				ngModel.$validators.comparaCom = function(modelValue) {
					return (modelValue == scope.comparaCom);
				};

				scope.$watch("comparaCom", function() {
					ngModel.$validate();
				})
			}
		}
	}

})();