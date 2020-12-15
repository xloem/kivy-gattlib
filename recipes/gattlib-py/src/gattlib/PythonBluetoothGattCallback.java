import java.net.ConnectException;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CancellationException;
import java.util.concurrent.ExecutionException;
import java.util.HashMap;
import java.util.UUID;

import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothProfile;

public final class PythonBluetoothGattCallback extends BluetoothGattCallback
{
    public static final class Status extends Exception
    {
        public final int code;
        public Status(int code)
        {
            super(codeToString(code));
            this.code = code;
        }

        public static String codeToString(int status)
        {
                switch (status) {
                case BluetoothGatt.GATT_CONNECTION_CONGESTED:
                    return "CONNECTION_CONGESTED";
                case BluetoothGatt.GATT_FAILURE:
                    return "FAILURE";
                case BluetoothGatt.GATT_INSUFFICIENT_AUTHENTICATION:
                    return "INSUFFICIENT_AUTHENTICATION";
                case BluetoothGatt.GATT_INSUFFICIENT_ENCRYPTION:
                    return "INSUFFICIENT_ENCRYPTION";
                case BluetoothGatt.GATT_INVALID_ATTRIBUTE_LENGTH:
                    return "INVALID_ATTRIBUTE_LENGTH";
                case BluetoothGatt.GATT_INVALID_OFFSET:
                    return "INVALID_OFFSET";
                case BluetoothGatt.GATT_READ_NOT_PERMITTED:
                    return "READ_NOT_PERMITTED";
                default:
                    return "UNRECOGNISED ERROR CODE";
                }
        }
    }

    private CompletableFuture<BluetoothGatt> future;
    private HashMap<UUID,Runnable> notifiees;
        
    public PythonBluetoothGattCallback()
    {
        reset();
    }

    public void subscribe(UUID uuid, Runnable runnable)
    {
        notifiees.put(uuid, runnable);
    }

    public void unsubscribe(UUID uuid)
    {
        notifiees.remove(uuid);
    }

    public void reset()
    {
        future = new CompletableFuture<BluetoothGatt>();
    }

    public BluetoothGatt waitFor() throws ExecutionException, CancellationException
    {
        // this approach of wrapping futures could likely be heavily simplified by
        // somebody more familiar with java or python; please do so if interested.
        // i noticed java has a 'synchronized' primitive, and inherent notify/wait
        // methods on every object.  or the concept could be moved into python,
        // which would be easier if PythonJavaClass provided for inheritance.
        while (true) {
            try {
                return future.get();
            } catch(InterruptedException e) {}
        }
    }

    @Override
    public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState)
    {
        if (status == 0) {
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                future.complete(gatt);
            }
        } else { // failure
            if (newState != BluetoothProfile.STATE_CONNECTED) {
                future.completeExceptionally(new Status(status));
            }
        }
    }

    @Override
    public void onServicesDiscovered(BluetoothGatt gatt, int status)
    {
        if (status == 0) {
            future.complete(gatt);
        } else {
            future.completeExceptionally(new Status(status));
        }
    }

    @Override
    public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status)
    {
        if (status == 0) {
            future.complete(gatt);
        } else {
            future.completeExceptionally(new Status(status));
        }
    }

    @Override
    public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic)
    {
        Runnable notifiee = notifiees.getOrDefault(characteristic.getUuid(), null);
        if (notifiee != null) {
            notifiee.run();
        }
    }
}
