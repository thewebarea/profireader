(function (angular) {
    'use strict';
    if (!angular) {
        throw 'No angular found';
    }

    var AppendParameter = function (url, var_val) {
        var hashpart =  url.match(/^([^#]*)(#(.*))?$/)
        var ret = hashpart[1] + (hashpart[1].match(/\?/) ? '&' : '?') + var_val + hashpart[2]
        return ret
    };

    var cloneIfExistsAttributes = function (cloneto, defaultparams, params) {

        $.each(defaultparams, function (ind, val) {
            cloneto[ind] = ((typeof params[ind] === 'undefined') ? val : params[ind]);
        });
        return cloneto;
    };

    var cloneIfExistsCallbacks = function (cloneto, defaultparams, params, $scope) {

        $.each(defaultparams, function (ind, val) {
            cloneto[ind] = ((typeof params[ind] === 'undefined') ? val : $scope[ind]);
        });
        return cloneto;
    };


    // url builders


    var retfirtsytapam = function (p, d) {
        return function (p, d) {
            return p
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
                    found = (action ? modelsForValidation[ind]['scope'][method](action) : modelsForValidation[ind]['scope'][method]());
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
                    'afUrlLoad': AppendParameter(params['af-url'], 'action=load'),
                    'afUrlValidate': AppendParameter(params['af-url'], 'action=validate'),
                    'afUrlSave': AppendParameter(params['af-url'], 'action=save')
                }, attrs);


                cloneIfExistsAttributes(params, {
                    'afDebounce': '500',
                    'afLoadResult': (attrs.ngModel + '_original'),
                    'afValidationResult': attrs.ngModel + '_validation',
                    'afSaveResult': attrs.ngModel + '_saved',
                    'afState': attrs.ngModel + '_state'
                }, attrs);

                params['afDebounce'] = parseInt(params['afDebounce']);
                if (params['afDebounce'] <= 0) params['afDebounce'] = 500;

                var trivialbefore = function () {
                    return function (model, default_function) {
                        return model;
                    }
                };

                var defaultCallbacks = {
                    afBeforeLoad: trivialbefore,
                    afBeforeValidate: trivialbefore,
                    afBeforeSave: trivialbefore,
                    afAfterLoad: function () {
                        return function (resp) {
                            $scope.model = cloneObject(resp);
                            setInParent('afLoadResult', cloneObject(resp));
                            return true;
                        }
                    },
                    afAfterValidate: function () {
                        return function (resp) {
                            setInParent('afValidationResult', cloneObject(resp));
                            if (resp['errors']) {
                                setInParent('afState', !resp['errors'] || Object.keys(resp['errors']).length ? 'invalid' : 'valid');
                                return true;
                            }
                            else {
                                return false;
                            }
                        }
                    },
                    afAfterSave: function () {
                        return function (resp) {
                            setInParent('afSaveResult', cloneObject(resp));
                            return true;
                        };
                    }
                };

                cloneIfExistsCallbacks(params, defaultCallbacks, attrs, $scope);

                function callCallback() {
                    var args = Array.prototype.slice.call(arguments);
                    var callbackkey = args.shift();
                    args.push(defaultCallbacks[callbackkey]());
                    var func = params[callbackkey]();
                    if (func === undefined) {
                        func = defaultCallbacks[callbackkey]();
                    }
                    var ret = func.apply($parent, args);
                    return ret;
                }

                var setInParent = function (ind, val) {
                    $parent[params[ind]] = val;
                };


                var func1 = function (action, statebefore, ok, notok) {
                    //debugger;
                    try {
                        var dataToSend = callCallback('afBefore' + action, $scope['model']);
                        var url = params['afUrl' + action];

                        setInParent('afState', statebefore);
                        $ok(url, dataToSend ? dataToSend : {},
                            function (resp, errorcode, httpresp) {
                                try {
                                    var ret = callCallback('afAfter' + action, resp);
                                    ok(ret);
                                }
                                catch (e) {
                                    notok(resp, e);
                                }
                            },
                            function (resp, errorcode, httpresp) {
                                notok(resp, errorcode);
                            });
                        return true;
                    }
                    catch (e) {
                        notok(undefined, e);
                    }


                };

                setInParent('afState', 'init');

                $scope.load = function () {
                    if ($scope.isActionAllowed('load')) {
                        func1('Load', 'loading',
                            function (resp) {
                                //$parent[attrs.ngModel] =  cloneObject(resp);
                                //$parent.$watch(attrs.ngModel, watchfunc, true);
                                //ctrl.$setViewValue(cloneObject(resp));
                                //ctrl.$render();
                                $af.$storeModelForValidation(ctrl, $scope);
                                setInParent('afState', 'clean');
                                //!!!$scope.$watch('model', watchfunc, true);
                            },
                            function (resp) {
                                setInParent('afState', 'loading_failed');
                            });
                    }
                    else {
                        console.error('called method `load` is forbidden for model because current model is in state: `' + $parent[params['afState']] + '`');
                    }
                };

                $scope.validate = function () {
                    if ($scope.isActionAllowed('validate')) {
                        func1('Validate', 'validating',
                            function (resp) {
                                if ($parent[params['afState']] === 'validating') {
                                    setInParent('afState', 'valid');
                                }
                            },
                            function (resp) {
                                setInParent('afState', 'validating_failed');
                            });
                    }
                    else {
                        console.error('called method `validate` is forbidden for model because current model is in state: `' + $parent[params['afState']] + '`. debouncing validation');
                        debouncedvalidate();
                    }
                };

                $scope.save = function () {
                    if ($scope.isActionAllowed('save')) {
                        func1('Save', 'saving',
                            function (resp) {
                                setInParent('afState', 'clean');
                            },
                            function (resp) {
                                setInParent('afState', 'saving_failed');
                            })
                    }
                    else {
                        console.error('called method `save` is forbidden for model because current model is in state: `' + $parent[params['afState']] + '`');
                    }
                };

                var save_states = ['init', 'clean', 'saving_failed', 'valid', 'loading_failed'];
                var validate_or_load_states = save_states.slice(0);
                validate_or_load_states.push('dirty', 'validating_failed', 'invalid');
                $scope.isActionAllowed = function (action) {
                    if (action === 'load') {
                        return validate_or_load_states.indexOf($parent[params['afState']]) !== -1
                    }
                    if (action === 'validate') {
                        return validate_or_load_states.indexOf($parent[params['afState']]) !== -1
                    }
                    if (action === 'save') {
                        return save_states.indexOf($parent[params['afState']]) !== -1
                    }
                };

                $scope.load();

                var debouncedvalidate = _.debounce(function () {
                    $scope.validate();
                }, params['afDebounce']);

                var watchfunc = function (oldval, newval) {
                    //if (-1 !== ['clean', 'saving_failed', 'valid', 'loading_failed', 'dirty', 'validating_failed', 'invalid', 'saving', 'validating'].indexOf($parent[params['afState']])) {
                        setInParent('afState', 'dirty');
                        debouncedvalidate();
                        //}
                };

                $scope.$watch('model', watchfunc, true);


            }
        };


    }]);


})(this.angular);
