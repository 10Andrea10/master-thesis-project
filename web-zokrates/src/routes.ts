import {Services} from './typings/services';

export async function initRoutes(services: Services) {
  const {router, executorMiddleware, userMiddleware} = services;

  // Execute the rollup
  router.post('/execute', executorMiddleware.executeRollup);

  router.post('/deregister', userMiddleware.deregisterUser);

  router.post('/register', userMiddleware.registerUser);

}
