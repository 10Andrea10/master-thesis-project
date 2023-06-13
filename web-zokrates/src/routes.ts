import {Services} from './typings/services';

export async function initRoutes(services: Services) {
  const {router, executorMiddleware, deregisterMiddleware} = services;

  // Execute the rollup
  router.post('/execute', executorMiddleware.executeRollup);

  router.post('/deregister', deregisterMiddleware.deregisterUser);

}
