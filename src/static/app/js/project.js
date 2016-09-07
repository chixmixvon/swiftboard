(function(){
    'use strict';

    angular.module('timetracker.project', [
            'ui.bootstrap',
            'ui.sortable',
        ])
        .factory('ProjectServices', ProjectServices)
        .factory('TaskServices', TaskServices)
        .factory('CommentServices', CommentServices)
        .controller('ProjectController', ProjectController)
        .controller('ProjectDetailController', ProjectDetailController)
        .directive('contenteditable', contenteditable)
    ;

    function ProjectController($scope, ProjectServices){
        ProjectServices.list();
        $scope.ProjectServices = ProjectServices;
    }

    function ProjectDetailController($rootScope, $scope, $state, $stateParams, ProjectServices, TaskServices) {
        var projectId = $stateParams.projectId;

        ProjectServices.detail(projectId);
        $rootScope.ProjectServices = ProjectServices;

        // task
        TaskServices.getTasks(projectId);
        $rootScope.TaskServices = TaskServices;
        $rootScope.ProjectServices = ProjectServices;

        $scope.sortableOptions = {
            connectWith: ".apps-container",
            stop: function(ev, ui) {
                var targetModel = ui.item.sortable.droptargetModel;
                var task = ui.item.sortable.model;
                var status;

                if (TaskServices.backlogs == targetModel) {
                    status = 0;
                } else if (TaskServices.todos == targetModel) {
                    status = 1;
                }
                 else if (TaskServices.progress == targetModel) {
                    status = 2;
                }
                 else if (TaskServices.resolved == targetModel) {
                    status = 3;
                }
                 else if (TaskServices.closed == targetModel) {
                    status = 4;
                }

                task.status = status;
                TaskServices.update(task);

                
            }
        };
  
    }

    function ProjectServices($http, $uibModal, $state, $stateParams, API_URL, TEMPLATE_URL) {
        var service = {
            projectsList: undefined,
            create: create,
            settings: settings,
            detail: detail,
            list: list,
            project: undefined,
            members: [],
            project_members: project_members,
            change_permission: change_permission,
            memberInitial: memberInitial,
            updateMembers: updateMembers,
            getMember: getMember
        }

        function create() {
            // create new project
            event.preventDefault();

            $uibModal.open({
                templateUrl: TEMPLATE_URL + 'board.form.html',
                controllerAs: 'ctrl',
                controller: function($scope, $uibModalInstance) {
                    // title of modal form
                    var self = this;
                    self.form = {};

                    self.submit = function() {
                        var data = {};
                        $http.post(API_URL + 'projects/', self.form).then(function(resp){
                            service.projectsList.push(resp.data);
                            $uibModalInstance.dismiss();
                        }, function(resp){
                            self.apiError = resp.data;
                        });
                    };
                }
            });
        }

        function memberInitial(member) {
            // 'John Cooper'  to JC
            return member.name.replace(/[^A-Z]/g, '');
        }

        function settings() {
            // change project settings
            event.preventDefault();

            $uibModal.open({
                templateUrl: TEMPLATE_URL + 'board.form.html',
                controllerAs: 'ctrl',
                controller: function($scope, $uibModalInstance) {
                    var self = this;
                    // title of modal form
                    self.title = service.project.name + ' Settings'
                    // initial data of form
                    self.form = angular.copy(service.project);

                    self.submit = function() {
                        var data = {};
                        $http.put(API_URL + 'projects/' + service.project.id + '/', self.form).then(function(resp){
                            service.project = resp.data;
                            $uibModalInstance.dismiss();
                        }, function(resp){
                            self.apiError = resp.data;
                        });
                    };
                }
            });
        }

        function project_members() {
            // display the list of project members
            event.preventDefault();
            $uibModal.open({
                templateUrl: TEMPLATE_URL + 'members.html',
                controllerAs: 'ctrl',
                controller: function($scope, $uibModalInstance) {
                    var self = this;
                    self.form = {};

                    self.permissions = [
                        {
                            id: 1,
                            name: "Admin",
                        },
                        {
                            id: 2,
                            name: "Manager",
                        },
                        {
                            id: 3,
                            name: "Developer",
                        },
                        {
                            id: 4,
                            "name": "Viewer",
                        },
                    ];
                    $scope.ProjectServices = service;
                    self.form['permission'] = self.permissions[0].id

                    self.submit = function() {
                        // add new member
                        self.form['project'] = service.project.id;

                        $http.post(API_URL + 'projects/' + service.project.id + '/members/', self.form).then(function(resp){
                            updateMembers(resp.data);
                            self.form['user'] = '';
                        }, function(resp){
                            self.apiError = resp.data;
                        });
                    };

                }
            });
        }

        function list() {
            // return list of projects
            return $http.get(API_URL + 'projects/').then(function(resp){
                service.projectsList = resp.data;
            });
        }

        function detail(id) {
            // return project detail
            return $http.get(API_URL + 'projects/' + id +'/').then(function(resp){
                service.project = resp.data;
                $state.current.title = service.project.name;

                // load members
                getMembers();
            });
        }

        function getMembers() {
            // return list of members
            return $http.get(API_URL + 'projects/' + service.project.id + '/members/').then(function(resp){
                service.members = resp.data;
            });
        }

        function updateMembers(data) {
            service.members.push(data);
        }

        function change_permission(member) {
            var data = {
                'user': member.email,
                'permission': member.selected,
                'project': member.project
            };
            
            $http.put(API_URL + 'projects/' + member.project + '/members/' + member.id + '/', data).then(function(resp){
                member = resp.data;
            }, function(resp){
                self.apiError = resp.data;
            });
        }

        function getMember(userId) {
            if (service.members) {
                return service.members.filter(function(user) {
                    if (user.user_id == userId) {
                        return user;
                    }
                })[0];
            }
        }

        return service;
    }

    function TaskServices($http, $rootScope, $uibModal, $state, $stateParams, API_URL, TEMPLATE_URL, ProjectServices, CommentServices) {
        var service = {
            create: create,
            tasks: undefined,
            backlogs: undefined,
            todos: undefined,
            progress: undefined,
            resolved: undefined,
            closed: undefined,
            getTasks: getTasks,
            task_status: task_status,
            update: update,
            preview: preview,
            reloadTasks: reloadTasks
        }

        function getTasks(projectId) {
            $http.get(API_URL + 'projects/' + projectId + '/tasks/').then(function(resp){
                service.tasks = resp.data;

                reloadTasks();
            });
        }

        function reloadTasks() {
            // update tasks
            service.backlogs = service.task_status(0);
            service.todos = service.task_status(1);
            service.progress = service.task_status(2);
            service.resolved = service.task_status(3);
            service.closed = service.task_status(4);
        }

        function updateTask(task) {
            service.tasks = service.tasks.map(function(item){
                if (item.id == task.id) {
                    item = task;
                }
                return item;
            });

            reloadTasks();
        }

        function task_status(status) {
            if (service.tasks) {
                return service.tasks.filter(function(item){
                    if (item.status == status) {
                        return item;
                    }
                });
            }
        }

        function update(task) {
            var data = {
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'assignee': task.assignee,
                'project': task.project,
            }
            return $http.put(API_URL + 'projects/' + task.project + '/tasks/' + task.id + '/', data);
        }

        function create(status){
            // create task
            $uibModal.open({
                templateUrl: TEMPLATE_URL + 'task.form.html',
                controllerAs: 'ctrl',
                controller: function($scope, $rootScope, $uibModalInstance) {
                    var self = this;
                    self.form = {};
                    self.activeForm = true;
                    // add null object to members
                    ProjectServices.members.unshift({'name': 'Unassigned'});

                    self.submit = function() {
                        var projectId = $rootScope.ProjectServices.project.id
                        self.form['project'] = projectId;
                        self.form['status'] = status;

                        $http.post(API_URL + 'projects/' + projectId + '/tasks/', self.form).then(function(resp){
                            service.tasks.push(resp.data);
                            // update
                            service.reloadTasks();

                            $uibModalInstance.dismiss();
                        }, function(resp){
                            self.apiError = resp.data;
                        });
                    };
                }
            });
        }

        function preview(task) {
            // create task
            $uibModal.open({
                templateUrl: TEMPLATE_URL + 'task.form.html',
                controllerAs: 'ctrl',
                controller: function($scope, $rootScope, $stateParams, $uibModalInstance, ProjectServices, CommentServices) {
                    // add null object to members
                    var projectId = $stateParams.projectId
                    ProjectServices.members.unshift({'name': 'Unassigned'});
                    $scope.ProjectServices = ProjectServices;
                    var self = this;
                    self.activeForm = false;
                    self.form = angular.copy(task);
                    self.assignee = ProjectServices.getMember(self.form.assignee);

                    CommentServices.get(projectId, task.id).then(function(resp){
                        self.comments = resp.data;
                    })

                    self.edit = function() {
                        // open an edit form
                        self.activeForm = true;
                    };

                    self.submit = function() {
                        // update task and return to preview section
                        service.update(self.form);
                        updateTask(self.form);
                        self.activeForm = false;
                    };

                    self.postComment = function(data) {
                        // allow user to post a comment
                        CommentServices.post(projectId, task.id, data).then(function(resp){
                            self.comments.unshift(resp.data);
                            data = {};
                        });
                    }
                }
            });
        }

        return service;
    }

    function CommentServices($http, $uibModal, API_URL, TEMPLATE_URL) {
        var service = {
            post: post,
            get:get
        }

        function post(projectId, taskId, data) {
            // post comment to a tasks
            data['task'] = taskId
            return $http.post(API_URL + 'projects/' + projectId + '/tasks/' + taskId + '/comments/', data);
        }

        function get(projectId, taskId) {
            // get task comments
            return $http.get(API_URL + 'projects/' + projectId + '/tasks/' + taskId + '/comments/');
        }

        return service;
    }

    // directive
    function contenteditable() {
            return {
              restrict: 'A', // only activate on element attribute
              require: '?ngModel', // get a hold of NgModelController
              link: function(scope, element, attrs, ngModel) {
                if(!ngModel) return; // do nothing if no ng-model

                // Specify how UI should be updated
                ngModel.$render = function() {
                  element.html(ngModel.$viewValue || '');
                };

                // Listen for change events to enable binding
                element.on('blur keyup change', function() {
                  scope.$apply(read);
                });
                read(); // initialize

                // Write data to the model
                function read() {
                  var html = element.html();
                  // When we clear the content editable the browser leaves a <br> behind
                  // If strip-br attribute is provided then we strip this out
                  if( attrs.stripBr && html == '<br>' ) {
                    html = '';
                  }
                  ngModel.$setViewValue(html);
                }
              }
            };
        }

})();