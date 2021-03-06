import Backbone from 'backbone';
import $ from 'jquery';
import _ from 'underscore';

// Views
import MainArea from './mainArea';
import LogArea from './logArea';

Backbone.$ = $;

// Main-Window view
var MainWindow = Backbone.View.extend({
    template: _.template($('#main-window-template').html()),
    initialize: function(options) {
        this.pipeline = options.pipeline;
        this.messageGroup = options.messageGroup;
    },
    render: function() {
        this.$el.html(this.template);
        this.mainArea = new MainArea({messageGroup: this.messageGroup, pipeline: this.pipeline});
        this.$el.find('#main-area').html(this.mainArea.render().$el);
        this.logArea = new LogArea({messageGroup: this.messageGroup});
        this.$el.find('#log-area').html(this.logArea.render().$el);
        return this;
    }
});

module.exports = MainWindow;