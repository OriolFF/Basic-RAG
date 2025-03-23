<!-- Delete any sections below when applicable. 
-->

## Automate Leak Canary

### Abstract

Have control of the leaks that arise in the development with the idea of listing them and solving them during the continuous integration

### Motivation

The goal of this RFC is to define agreements that allow us to follow a guide for the detection, collection and solution of the leaks that arise in our daily life. 

### Design Proposal

The idea is to create a reporter of the leak canary and when a leak appear send the traces to DataDog. We will enable or disable Leak Canary from the debug config view so that anyone with a debug version can do it and it can be a developer, QA or from the pipelines themselves.

This process is executed in the Nighly pipelines in order to have an updated report of the leaks and to be able to attack them before the release of a new version of the app.

Then we will create a use case to enable leak canary from the Debug Config view.

```kotlin
class SetLeakCanaryAvailabilityUseCase(private val leakUploader: LeakCanaryLeakUploader) {

    suspend operator fun invoke(enabled: Boolean) =
        setLeakCanary(enabled)

    private fun setLeakCanary(enabled: Boolean) {
        LeakCanary.config = when (enabled) {
            true -> LeakCanary.config.run { copy(dumpHeap = true, eventListeners = eventListeners + leakUploader) }
            false -> LeakCanary.config.copy(dumpHeap = false)
        }

        LeakCanary.showLeakDisplayActivityLauncherIcon(enabled)
    }
}
```

Next we will create a class in charge of uploading the leaks to DataDog.

```kotlin
class LeakCanaryLeakUploader(private val analytics: WallboxAnalytics) : EventListener {

    override fun onEvent(event: EventListener.Event) {
        when (event) {
            is EventListener.Event.HeapAnalysisDone.HeapAnalysisSucceeded -> uploadLeak(event.heapAnalysis)
            else -> DO_NOTHING
        }
    }

    private fun uploadLeak(heapAnalysis: HeapAnalysisSuccess) {
        analytics.track(
            Trace.InternalData(
                value = "Memory leak reporting",
                level = TrackingLevel.Warning,
                source = TrackingSource.App,
                params = HashMap(
                    heapAnalysis.applicationLeaks.associate { it.shortDescription to it.leakTraces.toString() }
                )
            )
        )
    }
}
```

#### Testing
This solution has been tested with QA using their pipeline to observe the behaviour of the app. After careful analysis, no bugs have been found and the pipelines have been executed correctly.

#### Analytics

This is how it looks in DataDog:

![Leak in DataDog](./Resources/AUTOMATE_LEAK_CANARY/data_dog_leak_canary.png)

#### Execution

MR: [Merge Request about PoC](https://gitlab.com/wallbox/mobile/wallbox_android_app/-/merge_requests/3972)

