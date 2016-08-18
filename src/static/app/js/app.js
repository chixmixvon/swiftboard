(function() {
    'use strict';

    angular.module('timetracker', [
            'ui.router',
            'ui.bootstrap',

            'timetracker.project',
        ])
        .config(routes)
        .constant('TEMPLATE_URL', '/static/app/templates/')
        .constant('API_URL', '/api/')
        .constant('AppConfig', {
            defaultTab: 'dashboard'
          })
        .run(initScopeData)
        .config( function run($httpProvider){
            // For CSRF token compatibility
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        })
    ;

    function routes($stateProvider, $urlRouterProvider, AppConfig, TEMPLATE_URL) {
        $urlRouterProvider.otherwise(function ($injector) {
            var $state = $injector.get('$state');
            if ($state.current.name === '') {
                // check current state empty, because some old non-angular ulrs may break routing
                $state.go(AppConfig.defaultTab);
            }
        });

        $stateProvider
            .state('legacy', {
                abstract: true,
                url: '',
                template: '<ui-view></ui-view>',
                title: 'TimeTracker'
            })
            .state('dashboard', {
                url: '/dashboard',
                templateUrl: TEMPLATE_URL + 'boards.html',
                controllerAs: 'ctrl',
                title: 'Dashboard',
                controller: 'ProjectController',
            })
            .state('board', {
                url: '/board/{projectId:int}',
                templateUrl: TEMPLATE_URL + 'board.html',
                controllerAs: 'ctrl',
                controller: 'ProjectDetailController',
                title: 'Loading',
            })
        ;
    }

    function initScopeData($rootScope, $state, $stateParams, TEMPLATE_URL) {
        $rootScope.pathHeader = TEMPLATE_URL + 'header.html';
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
    }

})();