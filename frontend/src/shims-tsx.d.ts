import Vue, { VNode } from 'vue';

declare global {
  namespace JSX {
    // tslint:disable completed-docs
    // tslint:disable no-empty-interface
    interface Element extends VNode {}
    // tslint:disable completed-docs
    // tslint:disable no-empty-interface
    interface ElementClass extends Vue {}
    // tslint:disable completed-docs
    interface IntrinsicElements {
      [elem: string]: any;
    }
  }
}
