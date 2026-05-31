import 'vue-router'
 
declare module 'vue-router' {
  interface RouteMeta {
    layout?: 'gost' | 'app'
    javno?: boolean
    uloga?: 'admin'
  }
}
