## App Initialization

This is our implementation for initializing different componsent needed for our application to work properly.

Whenever you need to initialize something you can create a new `Initializer`, eg `AnalyticsInitializer`, implementing the `AppInitializer` interface provided in the `core:common` module.

You can use the DI to get all the dependencies needed for the initialization and execute the initialization code in the init method that the interface will provide.

```kotlin
class AnalyticsInitializer @Inject constructor(
    private val analytics: Analytics
) : AppInitializer {

    override fun init() {
        // init analytics here
    }
}
```

This is just part of the requirement for the initialization.
To make sure that the initialization code will executed at the application startup you need to expose the new `Initializer` in a dedicated module with the `IntoSet` annotation like follow:

```kotlin
@Module
@InstallIn(SingletonComponent::class)
interface InitializerModule {

    @Binds
    @IntoSet
    fun provideAnalyticsInitializer(impl: AnalyticsInitializer): AppInitializer
}
```

In this way dagger multibinding is going to collect all the different `AppInitializer` for us into a set of Initializers that the application will use and execute in the `onCreate` method.

The `Initializer` and the `InitializerModule` can be placed in a different module, eg you could put the `AnalyticsInitializer` in a `core:analytics` module without the need of specifiying anything in the app module.

Another small trick.
If you don't have any code to execute is not mandatory to implement the `init()` method of the `AppInitializer` because the default implementation is `fun init() = Unit`.
So in this case if you just need to make sure that your class is loaded at the application start but you don't have nothing to execute you can directly extend the `AppInitializer` without the need of having a separate class for the initialization.
