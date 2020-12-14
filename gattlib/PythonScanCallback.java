import java.util.List;

import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;

//import android.widget.Toast;
//import org.kivy.android.PythonActivity;

public class PythonScanCallback extends ScanCallback
{
    public interface Interface
    {
        public void onScanFailed(int code);
        public void onScanResult(ScanResult result);
    }
    private Interface callback;

    //private void toast(final String text) {
    //    PythonActivity.mActivity.runOnUiThread(new Runnable () {
    //        public void run() {
    //            Toast.makeText(PythonActivity.mActivity, text, Toast.LENGTH_SHORT).show();
    //        }
    //    });
    //}

    public PythonScanCallback(Interface pythonCallback)
    {
        callback = pythonCallback;
        //toast("AndroidScanCallback initialised");
    }

    @Override
    public void onBatchScanResults(List<ScanResult> results)
    {
        //toast("onBatchScanResults");
        for (ScanResult result : results) {
            callback.onScanResult(result);
        }
    }

    @Override
    public void onScanFailed(int errorCode)
    {
        //toast("onScanFailed");
        callback.onScanFailed(errorCode);
    }

    @Override
    public void onScanResult(int callbackType, ScanResult result)
    {
        //toast("onScanResult");
        callback.onScanResult(result);
    }

}
