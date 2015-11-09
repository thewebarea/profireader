(function (angular) {
    'use strict';
    if (!angular) {
        throw 'No angular found';
    }

    var AppendParameter = function (url, var_val) {
        return url + (url.match(/\?/) ? '&' : '?') + var_val;
    };

    var cloneIfExistsAttributes = function (cloneto, defaultparams, params) {

        $.each(defaultparams, function (ind, val) {
            cloneto[ind] = ((typeof params[ind] === 'undefined' || params[ind] === '') ? val : params[ind]);
        });
        return cloneto;
    };


    var cloneIfExistsCalculatedArguments = function (cloneto, defaultparams, params) {
        $.each(defaultparams, function (ind, val) {
            cloneto[ind] = ((typeof params[ind] === 'undefined' || params[ind] === '') ? val : params[ind]);
        });
        return cloneto;
    };

    // url builders


    var retfirtsytapam = function (p, d) {
        return function (p, d) {
            return p
        }
    };
    var defaultCallbacks = {

        afBeforeLoad: function () {
            return function (model, default_function) {
                return true
            }
        },

        afAfterLoad: function () {
            return function (resp, default_function) {
                return resp
            }
        },

        afBeforeValidate: function () {
            return function (model, default_function) {
                return model
            }
        },

        afAfterValidate: function () {
            return function (resp, default_function) {
                return resp
            }
        },

        afBeforeSave: function () {
            return function (model, default_function) {
                return model
            }
        },

        afAfterSave: function () {
            return function (resp, default_function) {
                return resp
            }
        }

    };


    angular.module('ajaxFormModule', []).factory('$af', ['$ok', function ($ok) {

        var modelsForValidation = [];

        var ret = {};

        ret.$storeModelForValidation = function (model, scope) {
            modelsForValidation.push({model: model, scope: scope});
        };

        ret.$replaceModelForValidation = function (oldval, newval) {
            var found = false;
            //$.each(modelsForValidation, function (ind, val) {
            //    if (val === oldval) {
            //        modelsForValidation[ind] = newval;
            //        found = ind;
            //    }
            //});
            //if (found === false) {
            //    ret.$storeModelForValidation(newval);
            //}
        };

        ret.$callDirectiveMethod = function (model, method, action) {
            var found = false;
            $.each(modelsForValidation, function (ind, val) {
                if (val && val['model'].$modelValue === model) {
                    found = (action ? modelsForValidation[ind]['scope'][method](action) : modelsForValidation[ind]['scope'][method](action));
                }
            });
            return null;
        };

        ret.save = function (model, action) {
            ret.$callDirectiveMethod(model, 'save');
        };
        ret.load = function (model) {
            ret.$callDirectiveMethod(model, 'load');
        };
        ret.validate = function (model) {
            ret.$callDirectiveMethod(model, 'validate');
        };
        ret.isActionAllowed = function (model) {
            ret.$callDirectiveMethod(model, 'isActionAllowed', action);
        };
        return ret;

    }]).directive('af', ['$af', '$ok', function ($af, $ok) {

        return {
            restrict: 'A',
            scope: {
                'model': '=ngModel',
                'afBeforeLoad': '&',
                'afAfterLoad': '&',
                'afBeforeValidate': '&',
                'afAfterValidate': '&',
                'afBeforeSave': '&',
                'afAfterSave': '&'
            },
            require: ['ngModel'],
            link: function ($scope, el, attrs, afModelCtrl) {

                console.log($scope, el, attrs, afModelCtrl);

                var $parent = $scope['$parent'];
                var ctrl = afModelCtrl[0];


                var params = {};

                // validation watch params
                //cloneIfExists(params, {
                //    afWatch: '',
                //    afValidateDebounce: '500'
                //}, attrs);

                //SetIfEmpty(params, 'afWatch', params['ngData']);
                //params['afDebounce'] = parseInt(params['afDebounce']);


                cloneIfExistsAttributes(params, {'af-url': window.location.href}, attrs);
                cloneIfExistsAttributes(params, {
                    'af-url-load': AppendParameter(params['af-url'], 'action=load'),
                    'af-url-validate': AppendParameter(params['af-url'], 'action=validate'),
                    'af-url-save': AppendParameter(params['af-url'], 'action=save')
                }, attrs);

                cloneIfExistsAttributes(params, {
                    'af-debounce': '500',
                    'af-load-result': (attrs.ngModel + '_original'),
                    'af-validation-result': attrs.ngModel + '_validation',
                    'af-save-result': attrs.ngModel + '_saved',
                    'af-state': attrs.ngModel + '_state'
                }, attrs);

                params['af-debounce'] = parseInt(params['af-debounce']);
                if (params['af-debounce'] <= 0) params['af-debounce'] = 500;

                cloneIfExistsCalculatedArguments(params, defaultCallbacks, $scope);

                console.log(params);


                function callCallback() {
                    var args = Array.prototype.slice.call(arguments);
                    var callbackkey = args.shift();
                    args.push(defaultCallbacks[callbackkey]);
                    var func = params[callbackkey]();
                    if (func === undefined) {
                        func = defaultCallbacks[callbackkey]();
                    }
                    var ret = func.apply($parent, args);
                    return ret;
                }

                var setInParent = function (ind, val) {
                    $parent[params[ind]] = val;
                }


                var func1 = function (action, statebefore, ok, notok) {

                    var dataToSend = callCallback('afBefore' + action, $scope['model']);
                    var url = params['af-url-' + action.toLowerCase()];

                    if (!dataToSend || !url) {
                        return false;
                    }

                    setInParent('af-state', statebefore);
                    $ok(url, dataToSend,
                        function (resp, errorcode, httpresp) {
                            var ret = callCallback('afAfter' + action, resp);
                            ok(ret);
                        },
                        function (resp, errorcode, httpresp) {
                            notok(resp);
                        });

                    return true;
                }

                setInParent('af-state', 'init');

                $scope.load = function () {
                    if ($scope.isActionAllowed('load')) func1('Load', 'loading',
                        function (resp) {
                            $af.$storeModelForValidation(ctrl, $scope);
                            $scope.model = cloneObject(resp);

                            //$parent[attrs.ngModel] =  cloneObject(resp);
                            //$parent.$watch(attrs.ngModel, watchfunc, true);
                            //ctrl.$setViewValue(cloneObject(resp));
                            //ctrl.$render();
                            setInParent('af-load-result', cloneObject(resp));
                            setInParent('af-state', 'clean');
                        },
                        function (resp) {
                            setInParent('af-state', 'loading_failed');
                        });
                };

                $scope.validate = function () {
                    if ($scope.isActionAllowed('validate')) {
                        func1('Validate', 'validating',
                            function (resp) {
                                if ($parent[params['af-state']] === 'validating') {
                                    setInParent('af-validation-result', cloneObject(resp));
                                    if (resp && resp['errors']) {
                                        setInParent('af-state', Object.keys(resp['errors']).length ? 'invalid' : 'valid');
                                    }
                                    else {
                                        setInParent('af-state', 'validating_failed');
                                    }
                                }
                            },
                            function (resp) {
                                setInParent('af-state', 'validating_failed');
                            });
                    }
                    else {
                        debouncedvalidate();
                    }
                };

                $scope.save = function () {
                    if ($scope.isActionAllowed('save')) func1('Save', 'saving',
                        function (resp) {
                            setInParent('af-save-result', cloneObject(resp));
                            if ($parent[params['af-state']] === 'saving') {
                                setInParent('af-state', 'clean');
                            }
                        },
                        function (resp) {
                            setInParent('af-state', 'saving_failed');
                        })
                };

                var save_states = ['init', 'clean', 'saving_failed', 'valid', 'loading_failed', 'saving_failed'];
                var validate_or_load_states = save_states.slice(0);
                validate_or_load_states.push('dirty', 'validating_failed', 'invalid');
                $scope.isActionAllowed = function (action) {
                    if (action === 'load') {
                        return validate_or_load_states.indexOf($parent[params['af-state']]) !== -1
                    }
                    if (action === 'validate') {
                        return validate_or_load_states.indexOf($parent[params['af-state']]) !== -1
                    }
                    if (action === 'save') {
                        return save_states.indexOf($parent[params['af-state']]) !== -1
                    }
                };

                $scope.load();

                var debouncedvalidate = _.debounce(function () {
                    $scope.validate();
                }, params['af-debounce']);

                var watchfunc = function (oldval, newval) {
                    setInParent('af-state', 'dirty');
                    debouncedvalidate();
                };

                $scope.$watch('model', watchfunc, true);
            }
        };


    }]);


})(this.angular);
